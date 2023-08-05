""" mcli create secret Entrypoint """
import argparse
import logging
from typing import Callable, Optional

from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models import MCLIPlatform, MCLISecret, SecretType
from mcli.objects.secrets.create.docker_registry import DockerSecretCreator
from mcli.objects.secrets.create.generic import EnvVarSecretCreator, FileSecretCreator
from mcli.objects.secrets.create.s3 import S3SecretCreator
from mcli.objects.secrets.create.ssh import SSHSecretCreator
from mcli.objects.secrets.platform_secret import PlatformSecret
from mcli.utils.utils_interactive import InputDisabledError, ValidationError, input_disabled
from mcli.utils.utils_logging import OK, console

logger = logging.getLogger(__name__)
INPUT_DISABLED_MESSAGE = ('Incomplete secret. Please provide a name, key and value if running with '
                          '`--no-input`. Check `mcli create env --help` for more information.')

CREATORS = {
    SecretType.docker_registry: DockerSecretCreator,
    SecretType.environment: EnvVarSecretCreator,
    SecretType.mounted: FileSecretCreator,
    SecretType.ssh: SSHSecretCreator,
    SecretType.s3_credentials: S3SecretCreator,
}


def create_new_secret(
    secret_type: SecretType,
    secret_name: Optional[str] = None,
    no_input: bool = False,
    **kwargs,
) -> int:
    kwargs.pop('func', None)

    with input_disabled(no_input):
        try:
            creator = CREATORS[secret_type]()
            secret = creator.create(name=secret_name, **kwargs)
            logger.info(f'{OK} Created secret: {secret.name}')
            sync_secret(secret)
            logger.info(f'{OK} Synced to all platforms')
        except MCLIConfigError:
            logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
            return 1
        except InputDisabledError:
            logger.error(INPUT_DISABLED_MESSAGE)
            return 1
        except ValidationError as e:
            logger.error(e)
            return 1

    return 0


def sync_secret(secret: MCLISecret):
    conf = MCLIConfig.load_config()

    # Sync to all known platforms
    platform_secret = PlatformSecret(secret)
    with console.status('Creating secret in all platforms...') as status:
        for platform in conf.platforms:
            with MCLIPlatform.use(platform):
                status.update(f'Creating secret in platform: {platform.name}...')
                platform_secret.create(platform.namespace)


def _add_common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--name',
        dest='secret_name',
        help='What you would like to call the secret. Must be unique',
    )
    parser.add_argument('--no-input', action='store_true', help='Do not query for user input')


def _add_docker_registry_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    docker_registry_parser = subparser.add_parser(
        'docker',
        help='Create a secret to let you pull images from a private Docker registry.',
    )
    _add_common_arguments(docker_registry_parser)
    docker_registry_parser.add_argument(
        '--username',
        dest='docker_username',
        help='Your username for the Docker registry',
    )
    docker_registry_parser.add_argument(
        '--password',
        dest='docker_password',
        help='Your password for the Docker registry. If possible, use an API key here.',
    )
    docker_registry_parser.add_argument(
        '--email',
        dest='docker_email',
        help='The email you use for the Docker registry',
    )
    docker_registry_parser.add_argument('--server', dest='docker_server', help='The URL for the Docker registry')
    docker_registry_parser.set_defaults(func=secret_handler, secret_type=SecretType.docker_registry)


def _add_ssh_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    ssh_parser = subparser.add_parser('ssh', help='Create a SSH Secret')
    _add_common_arguments(ssh_parser)
    ssh_parser.add_argument('--ssh-private-key', help='Path the private key of an SSH key-pair')
    ssh_parser.add_argument('--mount-path', help='Location in your workload at which the SSH key should be mounted')
    ssh_parser.set_defaults(func=secret_handler, secret_type=SecretType.ssh)


def _add_mounted_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    generic_mounted_parser = subparser.add_parser('mounted', help='Create a secret that will be mounted as a text file')
    _add_common_arguments(generic_mounted_parser)
    generic_mounted_parser.add_argument('--mount-path',
                                        help='Location in your workload at which the secret should be mounted')
    generic_mounted_parser.add_argument('--value', help='Secret data you\'d like to store at the chosen path')
    generic_mounted_parser.set_defaults(func=secret_handler, secret_type=SecretType.mounted)


def _add_env_var_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    generic_env_parser = subparser.add_parser(
        'env',
        help='Create a secret that will be mounted as an environment variable',
    )
    _add_common_arguments(generic_env_parser)
    generic_env_parser.add_argument('--key', help='The KEY in KEY=VALUE for your environment variable. Must be unique')
    generic_env_parser.add_argument('--value', help='The VALUE in KEY=VALUE for your environment variable')
    generic_env_parser.set_defaults(func=secret_handler, secret_type=SecretType.environment)


def _add_s3_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    s3_cred_parser = subparser.add_parser('s3', help='Create an S3 Credentials Secret')
    _add_common_arguments(s3_cred_parser)
    s3_cred_parser.add_argument('--config-file', help='Path to your S3 config file. Usually `~/.aws/config`')
    s3_cred_parser.add_argument('--credentials-file',
                                help='Path to your S3 credentials file. Usually `~/.aws/credentials`')
    s3_cred_parser.add_argument(
        '--mount-directory',
        help='Location in your workload at which your credentials and config files will be mounted')
    s3_cred_parser.set_defaults(func=secret_handler, secret_type=SecretType.s3_credentials)


def configure_secret_argparser(
    parser: argparse.ArgumentParser,
    secret_handler: Callable,
) -> None:

    subparser = parser.add_subparsers()

    # Docker registry
    _add_docker_registry_subparser(subparser, secret_handler)

    # SSH credentials
    _add_ssh_subparser(subparser, secret_handler)

    # Mounted secrets
    _add_mounted_subparser(subparser, secret_handler)

    # Environment variables
    _add_env_var_subparser(subparser, secret_handler)

    # S3 credentials
    _add_s3_subparser(subparser, secret_handler)
