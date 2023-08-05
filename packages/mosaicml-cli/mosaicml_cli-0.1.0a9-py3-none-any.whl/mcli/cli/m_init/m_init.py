""" m init Entrypoint"""
import textwrap
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from yaspin import yaspin
from yaspin.core import Yaspin

from mcli import config
from mcli.config import MCLIConfig
from mcli.models import ProjectConfig
from mcli.objects.projects.create.project_create import generate_new_project
from mcli.objects.projects.info.project_info import get_projects_directory, get_projects_list


class TimedText:

    def __init__(self, text):
        self.text = text
        self._start = datetime.now()

    def __str__(self):
        now = datetime.now()
        delta = now - self._start
        return f'{self.text} ({round(delta.total_seconds(), 1)}s)'


ok_prefix = '✅ '
fail_prefix = '💥 '


def sp_message(spinner: Yaspin, message: str, success: bool, indent='') -> None:
    message = ' ' + message
    if success:
        message = ok_prefix + message
    else:
        message = fail_prefix + message
    message = indent + message
    spinner.write(message)


def new_timed_spin(
    spinner: Yaspin,
    text: str,
    timed_text: bool = True,
    previously_ok: bool = True,
) -> None:
    if previously_ok:
        spinner.ok(ok_prefix)
    else:
        spinner.fail(fail_prefix)

    if timed_text:
        spinner.text = TimedText(text)
    else:
        spinner.text = text
    spinner.start()


def initialize_mcli(**kwargs) -> int:
    del kwargs
    print(
        textwrap.dedent("""
    ------------------------------------------------------
    Welcome to MCLI
    ------------------------------------------------------
    """))

    def short_sleep():
        time.sleep(0.2)

    with yaspin() as sp:
        sp.text = TimedText('Initializing MCLI...')
        time.sleep(0.5)
        new_timed_spin(spinner=sp, text='Configuring Projects...')

        configure_directories: List[Tuple[Path, str]] = [
            (config.MCLI_CONFIG_DIR, 'MCLI Config Directory'),
            (get_projects_directory(), 'MCLI Projects Directory'),
        ]

        for conf_path, conf_name in configure_directories:
            if not conf_path.exists():
                sp_message(sp, f'No {conf_name} Found...', False)
                conf_path.mkdir(parents=True, exist_ok=True)
                short_sleep()
                sp_message(sp, f'MCLI {conf_name} Generated', True)

        # Generate MCLI Config if not existing
        try:
            mcli_config = MCLIConfig.load_config()
        except Exception as _:  # pylint: disable=broad-except
            sp_message(sp, 'No MCLI Config Found...', False)
            mcli_config = MCLIConfig.generate_new_config()
            mcli_config.save_config()
            short_sleep()
            sp_message(sp, 'MCLI Config Generated', True)

        projects_list = get_projects_list()
        if len(projects_list) == 0:
            sp_message(sp, 'No Projects Found', False)
            sp.write('Generating initial project...')
            sp.stop()
            current_project = generate_new_project(fork_from=None)
            current_project.set_current_project()
            sp.start()
        else:
            new_timed_spin(spinner=sp, text='Checking existing projects...')
            sp.write('Checking for existing projects...')
            try:
                current_project = ProjectConfig.get_current_project()
            except Exception as _:  # pylint: disable=broad-except
                current_project = projects_list[0]
                current_project.set_current_project()
                sp.write(f'No current project set. Setting to {current_project.project}')

        sp.text = TimedText('Spinning for the purpose of spinning...')
        time.sleep(0.5)
        sp.ok('✅ ')
        sp.write('Done!')

    return 0
