"""Creators for ssh secrets"""
from pathlib import Path
from typing import Callable, Optional

from mcli.models import SECRET_MOUNT_PATH_PARENT, SecretType
from mcli.objects.secrets import MCLISSHSecret
from mcli.objects.secrets.create.base import SecretCreator, SecretValidationError
from mcli.objects.secrets.create.generic import FileSecretFiller, FileSecretValidator
from mcli.utils.utils_interactive import get_validation_callback, list_options
from mcli.utils.utils_logging import FAIL
from mcli.utils.utils_string_validation import validate_existing_filename


class SSHSecretFiller(FileSecretFiller):
    """Interactive filler for SSH secret data
    """

    @staticmethod
    def fill_private_key(validate: Callable[[str], bool]) -> str:
        return list_options(
            'Where is your private SSH key located?',
            options=[],
            helptext='Path to your private SSH key',
            pre_helptext=None,
            allow_custom_response=True,
            validate=validate,
        )


class SSHSecretValidator(FileSecretValidator):
    """Validation methods for SSH secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    @staticmethod
    def validate_private_key(key_path: str) -> bool:

        if not validate_existing_filename(key_path):
            raise SecretValidationError(
                f'{FAIL} File does not exist. File path {key_path} does not exist or is not a file.')
        return True


class SSHSecretCreator(SSHSecretFiller, SSHSecretValidator):
    """Creates SSH secrets for the CLI
    """

    def create(
        self,
        name: Optional[str] = None,
        mount_path: Optional[str] = None,
        ssh_private_key: Optional[str] = None,
    ) -> MCLISSHSecret:

        # Validate mount and ssh key
        if mount_path:
            self.validate_mount(mount_path)

        if ssh_private_key:
            self.validate_private_key(ssh_private_key)

        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.ssh, name=name)
        assert isinstance(secret, MCLISSHSecret)

        if not ssh_private_key:
            ssh_private_key = self.fill_private_key(get_validation_callback(self.validate_private_key))

        secret.mount_path = mount_path or self.fill_mount(str(SECRET_MOUNT_PATH_PARENT / secret.name),
                                                          get_validation_callback(self.validate_mount))

        with open(Path(ssh_private_key).expanduser().absolute(), 'r', encoding='utf8') as fh:
            secret.value = fh.read()

        return secret
