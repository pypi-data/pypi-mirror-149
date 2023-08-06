#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

""" MCLI Entrypoint """

import argparse
import itertools
import logging
import sys
from string import ascii_lowercase

import argcomplete

from mcli import config
from mcli.cli.m_clean.m_clean import clean_mcli
from mcli.cli.m_create.m_create import add_create_argparser
from mcli.cli.m_delete.m_delete import add_delete_argparser
from mcli.cli.m_get.m_get import add_get_argparser
from mcli.cli.m_init.m_init import initialize_mcli
from mcli.cli.m_init.m_init_kube import DEFAULT_RANCHER_ENDPOINT, initialize_k8s
from mcli.cli.m_interactive.m_interactive import add_interactive_argparser
from mcli.cli.m_run.m_run import add_run_argparser
from mcli.cli.m_sweep.m_sweep import add_sweep_argparser
from mcli.cli.m_use.m_use import add_use_argparser
from mcli.models import ProjectConfig
from mcli.utils.utils_logging import console_handler
from mcli.utils.utils_pypi import NeedsUpdateError, check_new_update_available
from mcli.version import print_version

logger = logging.getLogger('mcli')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


def get_config(**kwargs) -> int:
    """Gets the current project config and prints it out

    Args:
        **kwargs:
    """
    del kwargs
    current_project = ProjectConfig.get_current_project()
    print(current_project)
    return 0


def test_mcli(**kwargs) -> int:
    """Testing stub function

    Args:
        **kwargs:
    """
    conf = config.get_mcli_config()
    print(conf)
    del kwargs
    return 0


def add_root_commands(subparser: argparse._SubParsersAction,) -> None:
    """Adds root level commands to the CLI

    Args:
        subparser: The subparser to add commands to
    """
    config_parser: argparse.ArgumentParser = subparser.add_parser(
        'config', aliases=['c'], help='Printout the config of the current MCLI project')
    config_parser.set_defaults(func=get_config)
    init_parser: argparse.ArgumentParser = subparser.add_parser('init', aliases=['i'], help='Initialize MCLI')
    init_parser.set_defaults(func=initialize_mcli)

    kube_init_parser: argparse.ArgumentParser = subparser.add_parser(
        'init-kube',
        aliases=['ik'],
        help='Configure your Kubernetes clusters using Rancher. These calls require access to Rancher, which you '
        'should have as users of the MosaicML cloud.',
    )
    kube_init_parser.add_argument('--auth-token', default=None, help='Your Rancher API key bearer token')
    kube_init_parser.add_argument('--rancher-endpoint',
                                  default=None,
                                  help='The rancher instance URL, '
                                  f'e.g. {DEFAULT_RANCHER_ENDPOINT}')
    kube_init_parser.add_argument('--namespace',
                                  default=None,
                                  help='Your namespace within the clusters. If it '
                                  'doesn\'t exist, it\'ll be created for you.')
    kube_init_parser.set_defaults(func=initialize_k8s)

    version_parser: argparse.ArgumentParser = subparser.add_parser('version', help='MCLI Version')
    version_parser.set_defaults(func=print_version)

    if config.get_mcli_config().dev_mode:
        clean_parser: argparse.ArgumentParser = subparser.add_parser('clean', aliases=['cl'], help='Clean MCLI')
        clean_parser.add_argument('--remove_db', action='store_true', default=False, help='Delete the FeatureDB Also')
        clean_parser.set_defaults(func=clean_mcli)
        test_parser: argparse.ArgumentParser = subparser.add_parser('test', aliases=['t'], help='Test stub')
        test_parser.set_defaults(func=test_mcli)


def get_parser() -> argparse.ArgumentParser:
    """The main parser
    """

    # Add common `mcli` arguments to a parent parser. These should be used by all subparsers.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('-v', '--verbose', action='count', help='Increase CLI verbosity', default=0)
    parents = [common]

    parser = argparse.ArgumentParser(prog='mcli', parents=parents)
    subparser = parser.add_subparsers()

    def print_help(**kwargs):
        del kwargs
        parser.print_help()

    parser.set_defaults(func=print_help)

    add_root_commands(subparser=subparser)
    add_run_argparser(subparser=subparser)
    add_sweep_argparser(subparser=subparser)
    add_create_argparser(subparser=subparser)
    add_use_argparser(subparser=subparser)
    add_get_argparser(subparser=subparser, parents=parents)
    add_delete_argparser(subparser=subparser)

    try:
        conf = config.MCLIConfig.load_config()
        if conf.internal:
            add_interactive_argparser(subparser=subparser)
    except config.MCLIConfigError:
        pass

    return parser


def main() -> int:
    """The main entrypoint
    """

    parser = get_parser()
    aliases = list(ascii_lowercase) + [''.join(i) for i in itertools.product(ascii_lowercase, repeat=2)]
    argcomplete.autocomplete(
        parser,
        exclude=aliases,
        always_complete_options='long',  # type: ignore
    )

    try:
        check_new_update_available()
    except NeedsUpdateError:
        return 1

    args = parser.parse_args()

    if len(vars(args)) == 0:
        parser.print_help()
        return 0

    if args.verbose >= 1:
        logger.setLevel(logging.DEBUG)

    console_handler.markup = True

    var_args = vars(args)
    del var_args['verbose']
    try:
        return args.func(**var_args)
    except KeyboardInterrupt as k:
        del k
        print('\nExiting with Keyboard Interrupt')
        return 1
    except Exception as e:
        raise e


if __name__ == '__main__':
    sys.exit(main())
