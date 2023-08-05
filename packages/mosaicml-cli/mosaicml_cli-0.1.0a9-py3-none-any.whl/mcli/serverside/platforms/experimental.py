"""Experimental platform features"""
from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import List, Optional

from kubernetes import client

from mcli.serverside.job.mcli_job import MCLIK8sJob
from mcli.serverside.platforms.instance_type import InstanceType


class ExperimentalFlag(Enum):
    """ Enum class for experimental Flags """
    RDMA = 'rdma'

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def permitted() -> List[ExperimentalFlag]:
        """Get all experimental flags available to a user

        Returns:
            List[ExperimentalFlag]: List of available experimental flags
        """
        return list(ExperimentalFlag)


class PlatformExperimental(ABC):
    """Handles applying platform-specific experimental flags to a job"""

    def get_allowed_experimental_flags(self, instance: InstanceType) -> List[ExperimentalFlag]:
        """Get experimental flags supported by the instance

        Args:
            instance (InstanceType): Instance to check

        Returns:
            List[ExperimentalFlag]: List of supported experimental flags
        """
        return instance.extras.get('experimental', [])

    def apply_experimental_flags(
        self,
        kubernetes_job: MCLIK8sJob,
        instance: InstanceType,
        experimental_flags: Optional[List[ExperimentalFlag]] = None,
    ) -> None:
        """Apply experimental flags requested by the user

        Args:
            job_spec (MCLIK8sJob): Job to apply flags to
            instance (InstanceType): Instance to check for flag support
            experimental_flags (Optional[List[ExperimentalFlag]]):
                List of flags requested by the user. Defaults to None.
        """
        if not experimental_flags:
            return

        allowed_experimental_flags = self.get_allowed_experimental_flags(instance)
        for flag in experimental_flags:
            if flag not in ExperimentalFlag.permitted():
                raise PermissionError(f'User not permitted to use experimental flag {flag}')
            if flag == ExperimentalFlag.RDMA and flag in allowed_experimental_flags:
                # Add rmda/roce resource
                resources = {'limits': {}, 'requests': {}}
                if kubernetes_job.container.resources:
                    resources = kubernetes_job.container.resources.to_dict()
                resources['limits'].update({'rdma/roce': 1})
                resources['requests'].update({'rdma/roce': 1})
                kubernetes_job.container.resources = client.V1ResourceRequirements(**resources)
                #Set privileged security context
                if not kubernetes_job.container.security_context:
                    kubernetes_job.container.security_context = client.V1SecurityContext()
                kubernetes_job.container.security_context.privileged = True
                kubernetes_job.container.security_context.run_as_user = 0
                # Set to use host network
                kubernetes_job.pod_spec.host_network = True
                kubernetes_job.pod_spec.dns_policy = 'ClusterFirstWithHostNet'
                # Set the memlock ulimit to unlimted before running the user command
                assert isinstance(kubernetes_job.container.args, List) and len(kubernetes_job.container.args) == 1
                kubernetes_job.add_command(
                    command='ulimit -l unlimited',
                    error_message='Unable to set ulimit. Please ensure you are running as root.',
                    required=True,
                )
            else:
                if flag not in allowed_experimental_flags:
                    raise ValueError(f'Experimental flag {str(flag)} not allowed for instance {instance.name}. '
                                     f'Valid options are: {allowed_experimental_flags}.')
                else:
                    raise ValueError(
                        f'Unsupported experimental flag: {str(flag)}. Valid options '
                        f'are {ExperimentalFlag.permitted()}, though not all are supported on all platforms.')
