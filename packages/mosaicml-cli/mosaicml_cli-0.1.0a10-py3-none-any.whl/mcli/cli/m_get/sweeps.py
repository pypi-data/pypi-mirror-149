"""CLI getter for sweeps"""
import itertools
from dataclasses import dataclass
from typing import Generator, List

from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.cli.m_get.runs import RunDisplayItem
from mcli.config import MCLIConfig, MCLIConfigError
from mcli.utils.utils_kube import KubeContext, list_jobs_across_contexts
from mcli.utils.utils_logging import FAIL, console, err_console


@dataclass
class SweepDisplayItem(MCLIDisplayItem):
    name: str
    count: int


class MCLISweepDisplay(MCLIGetDisplay):
    """`mcli get sweeps` display class
    """

    def __init__(self, runs: List[RunDisplayItem]):
        self.runs = sorted(runs, key=MCLISweepDisplay._sort_func)

    @staticmethod
    def _sort_func(run: RunDisplayItem) -> str:
        return run.sweep

    def __iter__(self) -> Generator[SweepDisplayItem, None, None]:
        for name, sweep_runs in itertools.groupby(self.runs, key=MCLISweepDisplay._sort_func):
            if name == '-':
                continue
            yield SweepDisplayItem(name=name, count=len(list(sweep_runs)))


def get_sweeps(output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    del kwargs

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        err_console.print(
            f'{FAIL} MCLI not yet initialized. You must have at least one platform before you can get '
            'sweeps. Please run `mcli init` and then `mcli create platform` to create your first platform.')
        return 1

    if not conf.platforms:
        err_console.print(f'{FAIL} No platforms created. You must have at least one platform before you can get '
                          'sweeps. Please run `mcli create platform` to create your first platform.')
        return 1

    with console.status('Retrieving requested runs...'):
        contexts = [KubeContext(cluster=p.kubernetes_context, namespace=p.namespace, user='') for p in conf.platforms]

        # Query for requested jobs
        all_jobs = list_jobs_across_contexts(contexts=contexts)
        runs = [RunDisplayItem.from_spec(job) for job in all_jobs]

    display = MCLISweepDisplay(runs)
    display.print(output)
    return 0
