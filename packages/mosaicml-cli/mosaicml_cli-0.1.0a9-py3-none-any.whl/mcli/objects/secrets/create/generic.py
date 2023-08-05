"""Creators for generic secrets"""
from typing import Callable, Optional, Set

from mcli.config import MCLIConfig
from mcli.models.mcli_secret import SECRET_MOUNT_PATH_PARENT, MCLIGenericSecret, SecretType
from mcli.objects.secrets import MCLIEnvVarSecret, MCLIMountedSecret, MCLIS3Secret
from mcli.objects.secrets.create.base import SecretCreator, SecretValidationError, SecretValidator
from mcli.utils.utils_interactive import get_validation_callback, list_options
from mcli.utils.utils_logging import FAIL
from mcli.utils.utils_string_validation import validate_absolute_path, validate_secret_key


class GenericSecretFiller():
    """Interactive filler for secret data
    """

    @staticmethod
    def fill_value() -> str:
        return list_options(
            'What data would you like to store?',
            options=[],
            helptext='',
            pre_helptext=None,
            allow_custom_response=True,
        )


class GenericSecretValidator():
    """Validation methods for generic secret data
    """
    pass


class GenericSecretCreator(GenericSecretFiller, GenericSecretValidator):
    """Creates base generic secrets for the CLI
    """

    def create(self, name: Optional[str] = None, value: Optional[str] = None) -> MCLIGenericSecret:

        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.generic, name=name)
        assert isinstance(secret, MCLIGenericSecret)

        if not secret.value:
            secret.value = value or self.fill_value()

        return secret


class EnvVarSecretFiller():
    """Interactive filler for secret data
    """

    @staticmethod
    def fill_key(validate: Callable[[str], bool]) -> str:
        return list_options('If an environment variable is KEY=VALUE, what should be the KEY?',
                            options=[],
                            allow_custom_response=True,
                            pre_helptext=None,
                            validate=validate)


class EnvVarSecretValidator(SecretValidator):
    """Validation methods for env var secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    def __init__(self):
        super().__init__()
        self.existing_keys = self.get_existing_keys()

    def get_existing_keys(self) -> Set[str]:
        conf = MCLIConfig.load_config()
        env_keys = {ev.env_key for ev in conf.environment_variables}
        secret_keys = {s.env_key for s in self.existing_secrets if isinstance(s, MCLIEnvVarSecret) and s.env_key}
        return env_keys | secret_keys

    @staticmethod
    def validate_key_characters(key: str) -> bool:
        is_valid = validate_secret_key(key)
        if not is_valid:
            raise SecretValidationError(f'{FAIL} Invalid secret key. {is_valid.message}')
        return True

    @staticmethod
    def validate_key_available(key: str, existing_keys: Set[str]) -> bool:
        if key in existing_keys:
            raise SecretValidationError(f'{FAIL} Duplicate key. Environment variable key {key} already exists. '
                                        f'Please choose something not in {sorted(list(existing_keys))}.')
        return True

    def validate_key(self, key: str) -> bool:
        return self.validate_key_characters(key) and self.validate_key_available(key, self.existing_keys)


class EnvVarSecretCreator(EnvVarSecretFiller, EnvVarSecretValidator):
    """Creates env var secrets for the CLI
    """

    def create(
        self,
        name: Optional[str] = None,
        value: Optional[str] = None,
        key: Optional[str] = None,
    ) -> MCLIEnvVarSecret:

        # Validate key
        if key:
            self.validate_key(key)

        # Create generic secret
        generic_creator = GenericSecretCreator()
        generic_secret = generic_creator.create(name, value)

        # Fill key
        if not key:
            key = self.fill_key(get_validation_callback(self.validate_key))

        return MCLIEnvVarSecret.from_generic_secret(generic_secret, env_key=key)


class FileSecretFiller():
    """Interactive filler for secret data
    """

    @staticmethod
    def fill_mount(default: str, validate: Callable[[str], bool]) -> str:
        return list_options(
            'Where would you like the data to be mounted within your workload?',
            options=[],
            default_response=default,
            allow_custom_response=True,
            helptext=f'default: {default}',
            pre_helptext=None,
            validate=validate,
        )


class FileSecretValidator(SecretValidator):
    """Validation methods for mounted secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    def __init__(self):
        super().__init__()
        self.existing_mounts = self.get_existing_mounts()

    def get_existing_mounts(self) -> Set[str]:
        secret_paths = {
            s.mount_path for s in self.existing_secrets if isinstance(s, MCLIMountedSecret) and s.mount_path
        }
        s3_mounts = {
            s.mount_directory for s in self.existing_secrets if isinstance(s, MCLIS3Secret) and s.mount_directory
        }
        return secret_paths | s3_mounts

    @staticmethod
    def validate_mount_absolute(path: str) -> bool:
        is_valid = validate_absolute_path(path)
        if not is_valid:
            raise SecretValidationError(f'{FAIL} Invalid mount point. Mount must be an absolute path, '
                                        f'not {path}.')
        return True

    @staticmethod
    def validate_mount_available(path: str, existing_paths: Set[str]) -> bool:
        if path in existing_paths:
            path_str = '\n'.join(sorted(list(existing_paths)))
            raise SecretValidationError(f'{FAIL} Duplicate path. Mount path {path} already in use.'
                                        f'Please choose something not in: {path_str}.')
        return True

    def validate_mount(self, path: str) -> bool:
        return self.validate_mount_absolute(path) and self.validate_mount_available(path, self.existing_mounts)


class FileSecretCreator(FileSecretFiller, FileSecretValidator):
    """Creates mounted secrets for the CLI
    """

    def create(
        self,
        name: Optional[str] = None,
        value: Optional[str] = None,
        mount_path: Optional[str] = None,
    ) -> MCLIMountedSecret:

        # Validate key
        if mount_path:
            self.validate_mount(mount_path)

        # Create generic secret
        generic_creator = GenericSecretCreator()
        generic_secret = generic_creator.create(name, value)

        # Fill key
        if not mount_path:
            mount_path = self.fill_mount(str(SECRET_MOUNT_PATH_PARENT / generic_secret.name),
                                         get_validation_callback(self.validate_mount))

        return MCLIMountedSecret.from_generic_secret(generic_secret, mount_path=mount_path)
