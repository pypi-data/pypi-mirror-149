""" CLI Get options"""
import argparse
from typing import List, Optional

from mcli.cli.m_get import get_environment_variables, get_platforms, get_projects, get_secrets, get_sweeps
from mcli.cli.m_get.display import OutputDisplay
from mcli.cli.m_get.runs import get_runs_argparser


def get_entrypoint(parser, **kwargs) -> int:
    del kwargs
    parser.print_help()
    return 0


def add_common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-o',
                        '--output',
                        type=OutputDisplay,
                        choices=list(OutputDisplay),
                        default=OutputDisplay.TABLE,
                        metavar='FORMAT',
                        help=f'Output display format. Should be one of {list(OutputDisplay)}')


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers(title='gettable objects',
                                       description='Get information on ',
                                       help='Some extra help',
                                       metavar='OBJECT')
    parser.set_defaults(func=get_entrypoint, parser=parser)

    projects_parser = subparsers.add_parser('projects', aliases=((((['project'])))), help='Get Project')
    add_common_arguments(projects_parser)
    projects_parser.set_defaults(func=get_projects)

    platform_parser = subparsers.add_parser('platforms', aliases=['platform'], help='Get Platforms')
    add_common_arguments(platform_parser)
    platform_parser.set_defaults(func=get_platforms)

    environment_parser = subparsers.add_parser('env', aliases=['environment'], help='Get Environment Variables')
    add_common_arguments(environment_parser)
    environment_parser.set_defaults(func=get_environment_variables)

    secrets_parser = subparsers.add_parser('secrets', aliases=['secret'], help='Get Secrets')
    add_common_arguments(secrets_parser)
    secrets_parser.set_defaults(func=get_secrets)

    runs_parser = get_runs_argparser(subparsers)
    add_common_arguments(runs_parser)

    sweeps_parser = subparsers.add_parser('sweeps', aliases=['sweep'], help='Get Sweeps')
    add_common_arguments(sweeps_parser)
    sweeps_parser.set_defaults(func=get_sweeps)

    return parser


def add_get_argparser(subparser: argparse._SubParsersAction,
                      parents: Optional[List[argparse.ArgumentParser]] = None) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Get parser to
    """
    del parents

    get_parser: argparse.ArgumentParser = subparser.add_parser(
        'get',
        aliases=['g'],
        help='Get info about objects created with mcli',
    )
    get_parser = configure_argparser(parser=get_parser)
    return get_parser
