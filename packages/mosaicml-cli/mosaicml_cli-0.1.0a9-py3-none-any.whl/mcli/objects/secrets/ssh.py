""" SSH Secret Type """
from dataclasses import dataclass
from typing import Dict, Optional

from kubernetes import client

from mcli.objects.secrets import MCLIMountedSecret
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob


@dataclass
class MCLISSHSecret(MCLIMountedSecret):
    """Secret class for ssh private keys that will be mounted to run pods as a file

    Overrides Git SSH Command to use the SSH key
    """
    ssh_private_key: Optional[str] = None

    def __post_init__(self):
        if self.ssh_private_key and not self.value:
            with open(self.ssh_private_key, 'r', encoding='utf8') as fh:
                self.value = fh.read()

    def unpack(self, data: Dict[str, str]):
        if 'ssh-privatekey' in data:
            data.setdefault('value', data['ssh-privatekey'])
        return super().unpack(data)

    def pack(self) -> Dict[str, str]:
        packed = super().pack()
        if self.ssh_private_key:
            packed['ssh-privatekey'] = packed['value']
        return packed

    def add_to_job(self, kubernetes_job: MCLIK8sJob, permissions: int = 256) -> bool:
        super().add_to_job(kubernetes_job=kubernetes_job, permissions=permissions)
        git_ssh_command_var = client.V1EnvVar(
            name='GIT_SSH_COMMAND',
            value=f'ssh -o StrictHostKeyChecking=no -i {self.mount_path}',
        )
        kubernetes_job.add_env_var(git_ssh_command_var)
        return True
