""" MCLI Git Repo Integration """
from dataclasses import dataclass
from typing import Optional

from mcli.models import MCLIIntegration
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob


@dataclass
class MCLIGitRepoIntegration(MCLIIntegration):
    """Git Repository Integration
    """
    git_repo: str
    git_branch: Optional[str] = None
    path: Optional[str] = None
    ssh_install: Optional[bool] = True
    pip_install: Optional[str] = None

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        clone_command = 'git clone '
        if self.git_branch:
            clone_command += f' -b {self.git_branch}'

        if self.ssh_install:
            clone_command += f' git@github.com:{self.git_repo}.git'
        else:
            clone_command += f' https://github.com/{self.git_repo}.git'

        clone_path = self.path
        if self.path is None:
            repo_split = self.git_repo.split('/')
            assert len(repo_split) == 2, 'Git repos should have the form organization/repo'
            clone_path = repo_split[1]

        clone_command += f' {clone_path}'

        if self.pip_install:
            # This is a hack to workaround issues with displaying progress bars in the
            # kubernetes python API for log viewing. We can remove this when logs are provided
            # through MAPI rather than the kube API directly
            # TODO: Remove this modification
            if '--progress-bar' not in self.pip_install:
                self.pip_install = f'{self.pip_install} --progress-bar ascii'

            pip_install_command = f'pip install {self.pip_install}'
            full_pip_install_command = f'cd {clone_path} && {pip_install_command} && cd ..'
            kubernetes_job.add_command(
                full_pip_install_command,
                error_message=f'Unable to install the repo with: {pip_install_command}',
                required=True,
            )

        kubernetes_job.add_command(
            clone_command,
            error_message=f'Unable to clone git repo: {self.git_repo}',
            required=True,
        )

        return True
