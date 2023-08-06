"""Implementation of mcli get runs"""
from __future__ import annotations

import argparse
import datetime as dt
from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Optional

from mcli.api.model.run_model import RunStatus
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import MCLIConfig, MCLIConfigError
from mcli.utils.utils_kube import KubeContext, list_jobs_across_contexts
from mcli.utils.utils_kube_labels import label
from mcli.utils.utils_logging import FAIL, console, err_console


@dataclass
class RunDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for display purposes.
    """
    instance: str
    sweep: str
    created_time: dt.datetime
    status: RunStatus

    @classmethod
    def from_spec(cls, spec: Dict[str, Any]) -> RunDisplayItem:
        extracted = {'name': spec['metadata']['name']}
        labels = spec['metadata'].get('labels', {})
        extracted['instance'] = labels.get(label.mosaic.LABEL_INSTANCE, '-')
        extracted['sweep'] = labels.get(label.mosaic.LABEL_SWEEP, '-')

        extracted['created_time'] = dt.datetime.fromisoformat(spec['metadata']['creationTimestamp'])

        status = spec.get('status', {})
        run_status = RunStatus.UNKNOWN
        if status.get('succeeded') == 1:
            run_status = RunStatus.SUCCEEDED
        elif status.get('failed') == 1:
            run_status = RunStatus.FAILED
        extracted['status'] = run_status

        return cls(**extracted)


class MCLIRunDisplay(MCLIGetDisplay):

    def __init__(self, jobs: List[Dict[str, Any]]):
        self.jobs = jobs

    def __iter__(self) -> Generator[RunDisplayItem, None, None]:
        for spec in self.jobs:
            yield RunDisplayItem.from_spec(spec)


def get_runs(run_list: Optional[List[str]] = None,
             instance: Optional[str] = None,
             platform: Optional[str] = None,
             status: Optional[RunStatus] = None,
             sweep: Optional[str] = None,
             output: OutputDisplay = OutputDisplay.TABLE,
             sort_by: str = 'updated_time',
             **kwargs) -> int:
    """Get a table of ongoing and completed runs
    """
    del status
    del kwargs
    del sort_by

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        err_console.print(f'{FAIL} MCLI not yet initialized. You must have at least one platform before you can get '
                          'runs. Please run `mcli init` and then `mcli create platform` to create your first platform.')
        return 1

    if not conf.platforms:
        err_console.print(f'{FAIL} No platforms created. You must have at least one platform before you can get '
                          'runs. Please run `mcli create platform` to create your first platform.')
        return 1

    if run_list is not None:
        raise NotImplementedError

    # Filter platforms
    if platform is not None:
        chosen_platforms = [p for p in conf.platforms if p.name == platform]
        if not chosen_platforms:
            platform_names = [p.name for p in conf.platforms]
            err_console.print(f'{FAIL} Platform not found. Platform name should be one of {platform_names}, '
                              f'not "{platform}".')
            return 1
    else:
        chosen_platforms = conf.platforms

    labels = {}
    # Filter instances
    if instance is not None:
        labels[label.mosaic.LABEL_INSTANCE] = instance

    # Filter sweep
    if sweep is not None:
        labels[label.mosaic.LABEL_SWEEP] = sweep

    with console.status('Retrieving requested runs...'):
        contexts = [KubeContext(cluster=p.kubernetes_context, namespace=p.namespace, user='') for p in chosen_platforms]

        # Query for requested jobs
        all_jobs = list_jobs_across_contexts(contexts=contexts, labels=labels)

    display = MCLIRunDisplay(all_jobs)
    display.print(output)

    return 0


def get_runs_argparser(subparsers):
    """Configures the ``mcli get runs`` argparser
    """
    # mcli get runs
    run_examples: str = """Examples:
    $ mcli get runs

    NAME                         INSTANCE      SWEEP
    run-foo                      inst-g0-type  sweep-foo
    run-bar                      inst-g0-type  sweep-bar
    """
    runs_parser = subparsers.add_parser('runs',
                                        aliases=['run'],
                                        help='Get information on all of your existing runs across all platforms.',
                                        epilog=run_examples,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    runs_parser.add_argument('--platform', help='Filter to just runs on a specific platform')
    runs_parser.add_argument('--instance')
    runs_parser.add_argument('--sweep')
    runs_parser.set_defaults(func=get_runs)

    return runs_parser
