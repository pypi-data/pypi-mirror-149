""" Delete Secret or Env Variable """
import logging
from typing import Callable, Dict, List

from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models import MCLIPlatform
from mcli.objects.secrets.platform_secret import PlatformSecret, SecretManager
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_kube import (ContextCall, delete_config_map, delete_job, delete_service,
                                   list_config_maps_across_contexts, list_jobs_across_contexts,
                                   list_services_across_contexts)
from mcli.utils.utils_kube_labels import label
from mcli.utils.utils_logging import FAIL, OK, console
from mcli.utils.utils_string_validation import ensure_rfc1123_compatibility

logger = logging.getLogger(__name__)


def delete_environment_variable(variable_name: str, force: bool = False, **kwargs) -> int:
    del kwargs
    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    existing_env_variables = conf.environment_variables
    new_env_vars = [x for x in existing_env_variables if x.name != variable_name]
    if len(existing_env_variables) == len(new_env_vars):
        print(f'Unable to find env var with name: {variable_name}.'
              ' To see all env vars run `mcli get env`')
        return 1

    if not force:
        confirm = query_yes_no(f'Would you like to delete environment variable {variable_name}?')
        if not confirm:
            print('Canceling deletion.')
            return 1

    conf.environment_variables = new_env_vars
    conf.save_config()
    return 0


def delete_secret(secret_name: str, force: bool = False, **kwargs) -> int:
    """Delete the requested secret from the user's MCLI config and platforms

    Args:
        secret_name: Name of the secret to delete
        force: If True, do not request confirmation. Defaults to False.

    Returns:
        True if deletion was successful
    """
    del kwargs

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if not conf.platforms:
        logger.error(f'{FAIL} No platforms found. You must have at least 1 platform added before working with secrets.')
        return 1

    # Note, we could just attempt to delete and catch the error.
    # I think it's a bit cleaner to first check if the secret exists, but this will be a bit slower
    # This slowness should be OK for secrets since they are generally small in number

    ref_platform = conf.platforms[0]
    secret_manager = SecretManager(ref_platform)

    to_delete: Dict[str, PlatformSecret] = {}
    for platform_secret in secret_manager.get_secrets():
        if platform_secret.secret.name == secret_name:
            to_delete[platform_secret.secret.name] = platform_secret

    if not to_delete:
        logger.error(f'Unable to find secret with name: {secret_name}.'
                     ' To see all secrets run `mcli get secrets`')
        return 1

    if not force:
        confirm = query_yes_no(f'Would you like to delete secret {secret_name}?')
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion.')
            return 1

    success = []
    with console.status('Deleting secrets...') as status:
        for platform in conf.platforms:
            with MCLIPlatform.use(platform):
                status.update(f'Deleting secrets from {platform.name}...')
                success.extend([ps.delete(platform.namespace) for ps in to_delete.values()])

    if not all(success):
        logger.error(f'{FAIL} Could not delete secret: {secret_name}')
        return 1

    logger.info(f'{OK} Deleted secret: {secret_name}')
    return 0


def delete_platform(platform_name: str, force: bool = False, **kwargs) -> int:
    del kwargs

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    existing_platforms = conf.platforms
    new_platforms = [x for x in existing_platforms if x.name != platform_name]
    if len(existing_platforms) == len(new_platforms):
        print(f'Unable to find platform with name: {platform_name}.'
              ' To see all platforms run `mcli get platforms`')
        return 1
    if not force:
        confirm = query_yes_no(f'Would you like to delete platform {platform_name}?')
        if not confirm:
            print('Canceling deletion.')
            return 1
    conf.platforms = new_platforms
    conf.save_config()
    return 0


def delete_project(project_name: str, **kwargs) -> int:
    del kwargs

    # TODO: Fix projects implementation
    existing_projects = []
    found_projects = [x for x in existing_projects if x.project == project_name]
    if not found_projects:
        print(f'Unable to find project with name: {project_name}.'
              ' To see all projects run `mcli get projects`')
        return 1
    if len(existing_projects) == 1:
        print('Unable to delete the only existing project'
              ' To see all projects run `mcli get projects`')
        return 1
    if found_projects and len(found_projects) == 1:
        found_project = found_projects[0]
        return found_project.delete()

    return 1


def delete_run(run_name: str, force: bool = False, **kwargs):
    del kwargs

    if len(run_name) == 0:
        logger.error(f'{FAIL} Must specify a run name.')
    run_name = ensure_rfc1123_compatibility(run_name)

    labels = {}
    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if not conf.platforms:
        logger.error(f'{FAIL} No platforms found. You must have at least 1 platform added before working with runs.')
        return 1

    if not force:
        confirm = query_yes_no(f'Would you like to delete run {run_name}?')
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion.')
            return 1

    contexts = [p.to_kube_context() for p in conf.platforms]
    labels[label.mosaic.JOB] = run_name

    with console.status(f'Deleting run {run_name}...'):
        # Query for requested jobs, config maps, and services
        all_jobs, job_responses = list_jobs_across_contexts(contexts=contexts, labels=labels)
        _, config_map_responses = list_config_maps_across_contexts(contexts=contexts, labels=labels)
        _, service_responses = list_services_across_contexts(contexts=contexts, labels=labels)

        if len(all_jobs) == 0:
            logger.error(f'Unable to find run with name: {run_name}.'
                         ' To see all runs do `mcli get runs`')
            return 1

        # Okay not to do this async because there will be at most 3 calls (one per resource)
        def _perform_delete(responses: List[ContextCall], delete_func: Callable[[str, str], bool]) -> bool:
            for res in responses:
                for obj in res.response['items']:
                    name = obj['metadata']['name']
                    if res.context.namespace and not delete_func(name, res.context.namespace):
                        logger.error(f'{FAIL} Failed to delete run {run_name}.')
                        return False
            return True

        if not _perform_delete(job_responses, delete_job):
            return 1
        if not _perform_delete(config_map_responses, delete_config_map):
            return 1
        if not _perform_delete(service_responses, delete_service):
            return 1

    logger.info(f'{OK} Deleted run: {run_name}')
    return 0
