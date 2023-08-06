""" MCLI Integration APT Packages """
from dataclasses import dataclass
from typing import List

from mcli.models import MCLIIntegration
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob


@dataclass
class MCLIPipPackagesIntegration(MCLIIntegration):
    """APT Package Integration
    """
    packages: List[str]
    upgrade: bool = False

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        package_list = ' '.join(self.packages)
        kubernetes_job.add_command(
            f'pip install {package_list} --progress-bar ascii',
            error_message=f'Failed to pip install packages: {package_list}',
            required=True,
        )
        return True
