""" mcli create env Entrypoint """
import argparse
import logging
from typing import Callable, Optional, Set

from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models import MCLIEnvVar
from mcli.objects.secrets.env_var import MCLIEnvVarSecret
from mcli.objects.secrets.platform_secret import SecretManager
from mcli.utils.utils_interactive import (InputDisabledError, ValidationError, get_validation_callback, input_disabled,
                                          list_options)
from mcli.utils.utils_logging import FAIL, OK

logger = logging.getLogger(__name__)
INPUT_DISABLED_MESSAGE = ('Incomplete environment variable. Please provide a name, key and value if running with '
                          '`--no-input`. Check `mcli create env --help` for more information.')


class EnvVarValidationError(ValidationError):
    """Env var could not be configured with the provided values
    """


class EnvVarFiller():
    """Interactive filler for environment variable data
    """

    @staticmethod
    def _fill_any(text: str, validate: Callable[[str], bool]) -> str:
        return list_options(
            input_text=text,
            options=[],
            pre_helptext=' ',
            allow_custom_response=True,
            validate=validate,
        )

    @classmethod
    def fill_name(cls, validate: Callable[[str], bool]) -> str:
        return cls._fill_any('What would you like to call this environment variable?', validate)

    @classmethod
    def fill_key(cls, validate: Callable[[str], bool]) -> str:
        return cls._fill_any('If the environment variable is KEY=VALUE, what should its KEY be?', validate)

    @classmethod
    def fill_value(cls) -> str:
        return cls._fill_any('If the environment variable is KEY=VALUE, what should its VALUE be?', lambda x: True)


class EnvVarValidator():
    """Validation methods for environment variable data

    Raises:
        EnvVarValidationError: Raised for any validation error for environment variable data
    """

    @staticmethod
    def validate_env_name_available(name: str, existing_names: Set[str]) -> bool:
        if name in existing_names:
            raise EnvVarValidationError(
                f'{FAIL} Existing environment variable. Variable named {name} already exists. Please '
                f'choose something not in {sorted(list(existing_names))}')
        return True

    @staticmethod
    def validate_env_key_available(key: str, existing_keys: Set[str]) -> bool:
        if key in existing_keys:
            raise EnvVarValidationError(f'{FAIL} Existing environment key. Key named {key} already exists. Please '
                                        f'choose something not in {sorted(list(existing_keys))}')
        return True


class EnvVarCreator(EnvVarValidator, EnvVarFiller):
    """Creates environment variables for the CLI
    """

    def get_existing_secret_keys(self, conf: MCLIConfig) -> Set[str]:
        """Get keys from existing environment variable secrets

        Args:
            conf: MCLIConfig

        Returns:
            Set of env var keys

        TODO: This should include ALL env var keys added by other secrets + an exclude list from job creation
        """
        if not conf.platforms:
            return set()
        ref_platform = conf.platforms[0]
        secret_manager = SecretManager(ref_platform)
        keys = set()
        for platform_secret in secret_manager.get_secrets():
            if isinstance(platform_secret.secret, MCLIEnvVarSecret) and platform_secret.secret.env_key:
                keys.add(platform_secret.secret.env_key)

        return keys

    def create(self, name: Optional[str], key: Optional[str], value: Optional[str]) -> MCLIEnvVar:

        # Get existing variable names and keys
        conf = MCLIConfig.load_config()
        existing_variables = conf.environment_variables
        existing_variable_names = {x.name for x in existing_variables}
        existing_variable_keys = {x.env_key for x in existing_variables}
        existing_variable_keys = existing_variable_keys.union(self.get_existing_secret_keys(conf))

        # Validate inputs
        if name:
            self.validate_env_name_available(name, existing_variable_names)

        if key:
            self.validate_env_key_available(key, existing_variable_keys)

        # Fill in missing values
        if not name:
            name = self.fill_name(
                validate=get_validation_callback(self.validate_env_name_available, existing_variable_names))
        if not key:
            key = self.fill_key(
                validate=get_validation_callback(self.validate_env_key_available, existing_variable_keys))
        if not value:
            value = self.fill_value()

        return MCLIEnvVar(name=name, env_key=key, env_value=value)


def create_new_env_var(
    variable_name: Optional[str] = None,
    key: Optional[str] = None,
    value: Optional[str] = None,
    no_input: bool = False,
    **kwargs,
) -> int:
    """Create an environment variable

    All required variables can be provided directly. If they are not provided, they will
    be requested interactively from the user unless `no_input` is `True`.

    Args:
        variable_name: Name of the environment variable. Defaults to None.
        key: Environment variable key. Defaults to None.
        value: Environment variable value. Defaults to None.
        no_input: If True, all required data must be provided since no interactive user
            input is allowed. Defaults to False.

    Returns:
        0 if creation succeeded, else 1
    """
    del kwargs

    with input_disabled(no_input):
        try:
            creator = EnvVarCreator()
            new_env_var = creator.create(variable_name, key, value)
        except MCLIConfigError:
            logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
            return 1
        except InputDisabledError:
            logger.error(INPUT_DISABLED_MESSAGE)
            return 1
        except EnvVarValidationError as e:
            logger.error(e)
            return 1

        conf: MCLIConfig = MCLIConfig.load_config()
        conf.environment_variables.append(new_env_var)
        conf.save_config()
        logger.info(f'{OK} Created environment variable: {new_env_var.name}')

    return 0


def configure_env_var_argparser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--name',
        dest='variable_name',
        help='What you would like to call the environment variable. Must be unique',
    )
    parser.add_argument(
        '--key',
        help='The KEY in KEY=VALUE for your environment variable. Must be unique',
    )
    parser.add_argument(
        '--value',
        help='The VALUE in KEY=VALUE for your environment variable',
    )
