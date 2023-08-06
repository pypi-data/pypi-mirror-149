"""mcli logs entrypoint"""
import argparse
import json
import logging
import sys
from typing import Any, Dict, Tuple, cast

from kubernetes import client

from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models.mcli_platform import MCLIPlatform
from mcli.serverside.job.mcli_k8s_job_typing import MCLIK8sPod
from mcli.utils.utils_kube import (PodStatusEpilog, find_pods_by_label, stream_pod_logs, wait_for_pod_start,
                                   watch_pod_events)
from mcli.utils.utils_kube_labels import label
from mcli.utils.utils_logging import FAIL, INFO, console

logger = logging.getLogger(__name__)


def convert_pod_dict(pod_dict: Dict[str, Any]) -> MCLIK8sPod:
    """Convert pod dict to an MCLIK8sPod to make it nicer to work with
    """
    api_client = client.ApiClient()

    class FakeResp:
        data = json.dumps(pod_dict)

    pod = api_client.deserialize(FakeResp(), 'V1Pod')
    return cast(MCLIK8sPod, pod)


def find_pod_and_platform(run_name: str) -> Tuple[MCLIK8sPod, MCLIPlatform]:
    """Find the first pod for a given run and the platform in which it exists
    """
    conf = MCLIConfig.load_config()
    all_contexts = [platform.to_kube_context() for platform in conf.platforms]
    with console.status('Requesting run logs...'):
        context_pods = find_pods_by_label(all_contexts, {label.mosaic.JOB: run_name})
        if not context_pods:
            raise RuntimeError(f'Could not find run: {run_name}')
        pod = convert_pod_dict(context_pods.response['items'][0])
        platform = MCLIPlatform.from_kube_context(context_pods.context)

    return pod, platform


def get_logs(run_name: str, **kwargs) -> int:
    del kwargs

    try:
        pod, platform = find_pod_and_platform(run_name)
        with MCLIPlatform.use(platform):
            # Check run status
            status = pod.status.phase
            if status == 'Pending':
                logger.info(f'{INFO} Run {run_name} has not been scheduled')
                return 0
            if status == 'ContainerCreating':
                logger.info(f'{INFO} Waiting for run to start, press Ctrl+C to quit')
                with console.status('Waiting for run to start...') as status:
                    epilog = PodStatusEpilog(status)
                    last_event = watch_pod_events(platform.namespace, epilog, name=pod.metadata.name, timeout=300)
                    pod_created = last_event is not None and last_event.status == 'Started'
                    if pod_created:
                        status.update('Verifying pod has started...')
                        pod_created = wait_for_pod_start(pod.metadata.name, platform.namespace)

            for line in stream_pod_logs(pod.metadata.name, platform.namespace):
                print(line, file=sys.stdout)

    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1
    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.set_defaults(func=get_logs)
    parser.add_argument('run_name', metavar='RUN', help='RUn name')

    return parser


def add_log_parser(subparser: argparse._SubParsersAction):
    """Add the parser for retrieving run logs
    """

    log_parser: argparse.ArgumentParser = subparser.add_parser(
        'logs',
        help='Print the logs from a specific run',
        description='Print the logs from a specific run and optionally follow the logs of an ongoing run.',
    )
    log_parser = configure_argparser(log_parser)

    return log_parser
