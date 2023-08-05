""" Checks PyPi for version updates """

from __future__ import annotations

import textwrap
import time
from datetime import datetime, timedelta
from typing import NamedTuple, Optional

import requests

from mcli import config, version
from mcli.config import FeatureFlag, MCLIConfig, MCLIConfigError


class Version(NamedTuple):
    """ An Easier to work with Version Encapsulation"""
    major: int
    minor: int
    patch: int
    extras: str = ''

    def __lt__(self, o: object) -> bool:
        assert isinstance(o, Version)
        if self.major != o.major:
            return self.major < o.major
        if self.minor != o.minor:
            return self.minor < o.minor
        if self.patch != o.patch:
            return self.patch < o.patch
        if self.extras and not o.extras:
            return True
        if not self.extras and o.extras:
            return False

        if self.extras and o.extras:
            # alphas check
            # TODO: maybe more version semantics but for now lets only support alphas
            try:
                return int(self.extras.split('a')[1]) < int(o.extras.split('a')[1])
            # pylint: disable-next=bare-except
            except:
                return True
        return False

    def __eq__(self, o: object) -> bool:
        assert isinstance(o, Version)
        return self.major == o.major \
            and  self.minor == o.minor \
            and self.patch == o.patch \
            and self.extras == o.extras

    def __gt__(self, o: object) -> bool:
        assert isinstance(o, Version)
        return o < self

    @classmethod
    def from_string(cls, text: str) -> Version:
        """Parses a semantic version of the form X.Y.Z[a0-9*]?

        Does not use `v` prefix and only supports optional alpha version tags

        Args:
            text: The text to parse

        Returns:
            Returns a Version object
        """
        text = text.lstrip('v')
        major, minor, patch = text.split('.')
        extras = ''
        if not patch.isdigit():
            if 'a' in patch:
                extras = patch[patch.index('a'):]
                patch = patch[:patch.index('a')]
        return Version(
            major=int(major),
            minor=int(minor),
            patch=int(patch),
            extras=extras,
        )

    def __str__(self) -> str:
        return f'v{self.major}.{self.minor}.{self.patch}{self.extras}'

    @property
    def is_alpha(self) -> bool:
        return self.extras != ''


_current_version = Version(
    major=version.__version_major__,
    minor=version.__version_minor__,
    patch=version.__version_patch__,
    extras=version.__version_extras__,
)


def get_latest_package_version(
    package_name: str = 'mosaicml-cli',
    current_version: Version = _current_version,
) -> Version:
    """Gets the latest release version of mcli from PyPI

    Returns:
        Version tuple
    """
    try:
        r = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()
        version_number = r.get('info', {}).get('version', None)
        return Version.from_string(version_number)
    except:  # pylint: disable=bare-except
        return current_version


def get_latest_alpha_package_version(
    package_name: str = 'mosaicml-cli',
    current_version: Version = _current_version,
) -> Version:
    """Gets the latest alpha version of mcli from PyPI

    Returns:
        Version tuple
    """
    try:
        r = requests.get(f'https://pypi.org/pypi/{package_name}/json').json()
        version_numbers = r.get('releases', {}).keys()
        all_versions = sorted([Version.from_string(x) for x in version_numbers], reverse=True)
        return all_versions[0]
    except:  # pylint: disable=bare-except
        return current_version


class NeedsUpdateError(Exception):
    """Raised if mcli requires an update
    """


def _is_check_needed(last_checked: datetime, check_frequency: float) -> bool:
    """Determine if an upgrade check is needed
    """
    time_since = (datetime.now() - last_checked).total_seconds() / (60 * 60 * 24)
    return time_since >= check_frequency


def _update_check_time(conf: MCLIConfig, check_again_in: Optional[float] = None):
    """Update the last-checked time in the config

    Arguments:
        conf: The MCLI config
        check_again_in: Optional number of minutes in which to check for updates again.
            Defaults to the update check frequency
    """
    conf.last_update_check = datetime.now()
    if check_again_in is not None:
        conf.last_update_check = conf.last_update_check - timedelta(days=config.UPDATE_CHECK_FREQUENCY_DAYS,
                                                                    minutes=-1 * check_again_in)
    conf.save_config()


def check_new_update_available(
    package_name: str = 'mosaicml-cli',
    current_version: Optional[Version] = None,
) -> None:
    """Check if a new mcli package is available in pypi

    Doesn't check if:
    - User has checked recently
    - User is set as 'dev'

    Required upgrades if:
    - Behind >= 1 major version
    - Behind >= 1 minor version
    - Behind > 1 patch version
    - Behind and on an alpha release
    - An alpha tester with a new alpha version available

    Suggests upgrade if:
    - Behind 1 patch version

    Raises:
        NeedsUpdateError: Raised if the user is too far behind on updates
    """
    if current_version is None:
        # Lazy sets current_version for monkeypatched tests
        current_version = _current_version

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        return

    # Don't check if user is on 'dev mode'
    if conf.dev_mode:
        print('DEV: Skipping update check')
        return

    # Don't check if user checked recently
    alpha_tester: bool = conf.feature_enabled(FeatureFlag.ALPHA_TESTER)
    check_frequency: float = config.UPDATE_CHECK_FREQUENCY_DAYS if not alpha_tester else 2.0 / 24.0
    if not _is_check_needed(conf.last_update_check, check_frequency):
        return

    print('Checking for new MCLI updates')
    if current_version.is_alpha or alpha_tester:
        latest_version = get_latest_alpha_package_version(
            package_name=package_name,
            current_version=current_version,
        )
    else:
        latest_version = get_latest_package_version(
            package_name=package_name,
            current_version=current_version,
        )

    if current_version > latest_version:
        print('MCLI Version up to date! Prerelease found!\n')
        _update_check_time(conf)
        return

    if current_version == latest_version:
        print('MCLI Version up to date!\n')
        _update_check_time(conf)
        return

    print(
        textwrap.dedent(f"""
        New version of MCLI detected

        ------------------------------
        Local version: \t\t{current_version}
        Most recent version: \t{latest_version}
        ------------------------------

        """))
    if alpha_tester:
        print('Thanks for being an Alpha tester!')

    version_spec = f'=={str(latest_version).lstrip("v")}' if latest_version.is_alpha else ''
    version_update_required_message = textwrap.dedent(f"""
    Please update your mcli version to continue using mcli
    To do so, run:

    pip install --upgrade {package_name}{version_spec}
    """)

    # On an old alpha, so update is required
    if current_version.is_alpha:
        print(f'Pre-release out of date.\n{version_update_required_message}')
        raise NeedsUpdateError

    # A new alpha is available (only alpha testers will hit this)
    if latest_version.is_alpha:
        print(f'Pre-release update available.\n{version_update_required_message}')
        raise NeedsUpdateError

    if current_version.major != latest_version.major:
        print(f'Major version out of sync.\n{version_update_required_message}')
        raise NeedsUpdateError

    if current_version.minor != latest_version.minor:
        print(f'Minor version out of sync.\n{version_update_required_message}')
        raise NeedsUpdateError

    if latest_version.patch - current_version.patch >= 2:
        print(f'Patch version >= 2 versions out of date.\n{version_update_required_message}')
        raise NeedsUpdateError

    if latest_version.patch != current_version.patch:
        print('Patch version out of date.')
        print(
            textwrap.dedent(f"""
        You can continue, but we recommend updating mcli ASAP
        This message will reset every two hours

        To update mcli run:

        pip install --upgrade {package_name}{version_spec}

        Ctrl-c to exit and update now
        """))
        time.sleep(5)
        _update_check_time(conf, check_again_in=120)
    else:
        _update_check_time(conf)
