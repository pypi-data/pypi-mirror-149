""" mcli run Entrypoint """
import argparse
import logging
import textwrap
from typing import List, Optional

from mcli import config
from mcli.api.model.run_model import RunModel
from mcli.models import PartialRunInput, RunInput
from mcli.models.mcli_platform import MCLIPlatform
from mcli.serverside.job.mcli_job import MCLIJob
from mcli.serverside.platforms.experimental import ExperimentalFlag
from mcli.serverside.runners.runner import Runner
from mcli.utils.utils_kube import (LogParseError, PodStatusEpilog, get_pod_logs, wait_for_job_pods, wait_for_pod_start,
                                   watch_pod_events)
from mcli.utils.utils_logging import FAIL, INFO, OK, console

logger = logging.getLogger(__name__)


def run_entrypoint(
    file: str,
    experimental: Optional[List[ExperimentalFlag]] = None,
    priority: Optional[str] = None,
    tail: bool = True,
    **kwargs,
) -> int:
    del kwargs
    # TODO: Reintroduce experimental and priority
    del experimental
    del priority
    logger.info(
        textwrap.dedent("""
    ------------------------------------------------------
    Let's run this run
    ------------------------------------------------------
    """))

    partial_run_input = PartialRunInput.from_file(path=file)
    run_input = RunInput.from_partial_run_input(partial_run_input)
    mcli_job = run(run_input=run_input)

    with MCLIPlatform.use(mcli_job.platform) as platform:
        logger.info(f'{INFO} Run {mcli_job.run_name} submitted. Waiting for it to start...')
        logger.info(f'{INFO} Press Ctrl+C to quit and follow your run manually.')
        with console.status('Waiting for run to be scheduled...') as status:
            epilog = PodStatusEpilog(status)
            logger.debug(f'Getting pods for job: {mcli_job.unique_name}')
            pod_names = wait_for_job_pods(name=mcli_job.unique_name, namespace=platform.namespace)
            pod_name = pod_names[0]
            logger.debug(f'Found pod: {pod_name}')
            last_event = watch_pod_events(platform.namespace, epilog, name=pod_name, timeout=300)
            pod_created = last_event is not None and last_event.status == 'Started'
            if pod_created:
                status.update('Verifying pod has started...')
                pod_created = wait_for_pod_start(pod_name, platform.namespace)

        if pod_created:
            logger.info(f'{OK} Run {mcli_job.run_name} started')
            if tail:
                logger.info(f'{INFO} Following run logs. Press Ctrl+C to quit.\n')
                try:
                    _ = get_pod_logs(pod_name, platform.namespace, logger=logger)
                except LogParseError as e:
                    logger.error(e)
        else:
            # TODO: Figure out what else to do here. Where do we want to redirect people
            # to if we don't assume kubectl install?
            logger.warning('Waiting for run to spawn exceeded the timeout.')

    return 0


def run(run_input: RunInput) -> MCLIJob:
    if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
        run_model = RunModel.from_run_input(run_input=run_input)
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs.create_run import create_run
        if not create_run(run_model):
            logger.warning(f'{FAIL} Failed to persist run')

    # Populates the full MCLI Job including user defaults
    mcli_job = MCLIJob.from_run_input(run_input=run_input)

    runner = Runner()
    runner.submit(job=mcli_job,)
    return mcli_job


def add_run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser: argparse.ArgumentParser = subparser.add_parser(
        'run',
        aliases=['r'],
        help='Run stuff',
    )
    run_parser.set_defaults(func=run_entrypoint)
    _configure_parser(run_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-f',
        '--file',
        dest='file',
        help='File from which to load arguments.',
    )

    parser.add_argument(
        '--experimental',
        choices=ExperimentalFlag.permitted(),
        type=ExperimentalFlag,
        nargs='+',
        default=None,
        metavar='FLAG',
        help=
        'Enable one or more experimental flags. These flags are designed to take advantage of a specific feature that '
        'may still be too experimental for long-term inclusion in mcli.',
    )

    parser.add_argument(
        '--priority',
        choices=('low', 'standard', 'high'),
        help='Priority level at which runs should be submitted. '
        '(default None)',
    )

    parser.add_argument(
        '--no-tail',
        action='store_false',
        dest='tail',
        help='Do not automatically try to follow the run\'s logs',
    )
