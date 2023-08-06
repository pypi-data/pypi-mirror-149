""" mcli interactive Entrypoint """
import argparse
import logging
from typing import Dict, Optional

from mcli.config import MESSAGE, MCLIConfigError
from mcli.models.mcli_platform import MCLIPlatform
from mcli.models.run_input import PartialRunInput, RunInput
from mcli.serverside.job.mcli_job import MCLIJob
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.registry import PlatformRegistry
from mcli.serverside.runners.runner import Runner
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_kube import (PodStatusEpilog, connect_to_pod, wait_for_job_pods, wait_for_pod_start,
                                   watch_pod_events)
from mcli.utils.utils_logging import FAIL, INFO, OK, console
from mcli.utils.utils_types import get_hours_type

_MAX_INTERACTIVE_DURATION: float = 8

logger = logging.getLogger(__name__)


def get_interactive_platform(platform_str: Optional[str] = None) -> GenericK8sPlatform:
    """Gets an interactive-enabled platform

    If ``platform_str`` is not ``None``, then the corresponding Kubernetes platform is returned
    if it has interactive enabled. If not, it errors with a ``RuntimeError``. If ``platform_str``
    is ``None``, all possible interactive platforms are detected. If none exist, then a
    ``RuntimeError`` is thrown. If more than one exist, the user is prompted to choose one.

    Args:
        platform_str: Optional name of the platform on which to run the session. Defaults to None.

    Returns:
        A valid Kubernetes platform

    Raises:
        RuntimeError: Raised if a valid Kubernetes platform could not be found.
    """
    registry = PlatformRegistry()
    interactive_platforms: Dict[str, GenericK8sPlatform] = {}
    mcli_platform: Optional[MCLIPlatform] = None
    for pl in registry.platforms:
        if pl.name == platform_str:
            mcli_platform = pl
        k8s_platform = registry.get_k8s_platform(pl)
        if k8s_platform.interactive:
            interactive_platforms[pl.name] = k8s_platform

    if platform_str is not None:
        if mcli_platform is not None and (mcli_platform.name not in interactive_platforms):
            raise RuntimeError(f'Platform {platform_str} does not permit interactive sessions')
        assert mcli_platform is not None
        return interactive_platforms[mcli_platform.name]

    if not interactive_platforms:
        raise RuntimeError('None of your configured platforms permit interactive sessions. If you should have access '
                           'to one, make sure to create it using `mcli create platform`.')

    valid_mcli_platforms = list(interactive_platforms.keys())
    if len(valid_mcli_platforms) > 1:
        raise RuntimeError('Multiple platforms found that permit interactive sessions. Please specify one of '
                           f'{valid_mcli_platforms} with the --platform argument.')
    else:
        chosen_platform = valid_mcli_platforms[0]

    return interactive_platforms[chosen_platform]


def get_interactive_instance(platform: GenericK8sPlatform, num_gpus: int) -> InstanceType:
    """Get an instance with the requested number of GPUs

    Args:
        platform: Platform to run on
        num_gpus: Number of GPUs

    Raises:
        RuntimeError: Raised if no instance could be found

    Returns:
        Valid Instance
    """
    instance = platform.get_interactive_instance_from_gpus(num_gpus=num_gpus)
    if instance is None:
        valid_values = [instance.gpu_count for instance in platform.allowed_instances]
        raise RuntimeError(f'{FAIL} Could not find a suitable instance for {num_gpus}. '
                           f'Valid values are: {valid_values}.')
    return instance


def interactive_entrypoint(
    name: Optional[str] = None,
    num_gpus: int = 1,
    platform: Optional[str] = None,
    hours: float = 1,
    image: str = 'mosaicml/pytorch',
    confirm: bool = True,
    connect: bool = True,
    **kwargs,
) -> int:
    del kwargs

    try:
        chosen_platform = get_interactive_platform(platform)
        instance = get_interactive_instance(chosen_platform, num_gpus)
        if not name:
            name = f'interactive-{instance.gpu_type.value}-{num_gpus}'.lower()

        partial_run = PartialRunInput(
            run_name=name,
            platform=chosen_platform.platform_information.name,
            instance_type=instance.name,
            command=f'sleep {int(3600 * hours)}',
            image=image,
        )
        run_input = RunInput.from_partial_run_input(partial_run)

        mcli_job = MCLIJob.from_run_input(run_input=run_input)

        logger.info(f'{OK} Ready to submit a [bold]{num_gpus} GPU[/] interactive session for [bold]{hours} hour(s)[/] '
                    f'to platform [bold green]{chosen_platform.platform_information.name}[/]')
        if confirm:
            confirm = query_yes_no('Do you want to submit?')
            if not confirm:
                raise RuntimeError('Canceling!')

        runner = Runner()
        runner.submit(job=mcli_job)
        with MCLIPlatform.use(chosen_platform.platform_information) as mcli_platform:
            logger.info(f'{INFO} Interactive session submitted. Waiting for it to start...')
            logger.info(f'{INFO} Press Ctrl+C to quit and interact with your session manually.')
            with console.status('Waiting for workload to be scheduled...') as status:
                epilog = PodStatusEpilog(status)
                logger.debug(f'Getting pods for job: {mcli_job.unique_name}')
                pod_names = wait_for_job_pods(name=mcli_job.unique_name, namespace=mcli_platform.namespace)
                pod_name = pod_names[0]
                logger.debug(f'Found pod: {pod_name}')
                last_event = watch_pod_events(mcli_platform.namespace, epilog, name=pod_name, timeout=300)
                pod_created = last_event is not None and last_event.status == 'Started'
                if pod_created:
                    status.update('Verifying pod has started...')
                    pod_created = wait_for_pod_start(pod_name, mcli_platform.namespace)

            context = mcli_platform.to_kube_context()
            exec_cmd = f'kubectl --context {context.cluster} exec -it {pod_name} -- /bin/bash'
            if pod_created:
                if connect:
                    logger.info(f'{OK} Interactive session created. Attaching...')
                    logger.info(f'{INFO} Press Ctrl+C to quit attaching. Once attached, press Ctrl+D or type exit '
                                'to leave the session.')
                    connected = connect_to_pod(pod_name, context)
                    if not connected:
                        logger.warning(f'{FAIL} Could not connect to the interactive session.')
                        logger.warning(f'Please double-check that [bold]{context.cluster}[/] is your context and '
                                       f'[bold]{context.namespace}[/] is your correct namespace.')
                        logger.warning(f'If so, try manually running {exec_cmd}')
                else:
                    logger.info(f'{OK} Interactive session created. You can attach to it using:\n\n{exec_cmd}')
            else:
                get_pods_cmd = f'kubectl --context {context.cluster} get pods -w {pod_name}'
                logger.warning('Waiting for interactive session to spawn exceeded the timeout. You can monitor it '
                               f'using:\n\n{get_pods_cmd}\n\n'
                               f'Once the pod is "Running", you can attach to it using:\n\n{exec_cmd}')
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1
    except RuntimeError as e:
        logger.error(e)
        return 1

    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('--name',
                        default=None,
                        type=str,
                        help='Name for the interactive session. '
                        'Default: "interactive-<gpu type>-<num gpus>"')
    parser.add_argument('--num-gpus',
                        default=1,
                        type=int,
                        choices=(1, 2, 4),
                        help='Number of GPUs to run interactively. Default: %(default)s.')
    parser.add_argument('--platform',
                        default=None,
                        help='Platform where your interactive session should run. If you '
                        'only have one available, that one will be selected by default.')
    parser.add_argument('--hours',
                        default=1,
                        type=get_hours_type(_MAX_INTERACTIVE_DURATION),
                        help='Number of hours the interactive session should run. Default: %(default)s.')
    parser.add_argument('--image', default='mosaicml/pytorch', help='Docker image to use')
    parser.add_argument('-y', '--no-confirm', dest='confirm', action='store_false', help='Do not request confirmation')
    parser.add_argument('--no-connect',
                        dest='connect',
                        action='store_false',
                        help='Do not connect to the interactive session immediately.')

    parser.set_defaults(func=interactive_entrypoint)
    return parser


def add_interactive_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """

    interactive_parser: argparse.ArgumentParser = subparser.add_parser(
        'interactive',
        aliases=['int'],
        help='Get an interactive instance',
    )
    get_parser = configure_argparser(parser=interactive_parser)
    return get_parser
