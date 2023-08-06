# pylint: disable=duplicate-code

""" The base class for how a platform will operate """
from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

from kubernetes import client

from mcli.models import MCLIPlatform
from mcli.objects.secrets.platform_secret import SecretManager
from mcli.serverside.job.mcli_job import MCLIK8sJob, MCLIVolume
from mcli.serverside.platforms.experimental import ExperimentalFlag, PlatformExperimental
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.platform_instances import PlatformInstances

# types
Resources = Dict[str, int]
Description = Dict[str, Any]


class PlatformSetupError(Exception):
    """Raised if platform setup failed
    """


class PlatformCreationError(Exception):
    """Raised if platform setup failed
    """


class PlatformResourceHandler():
    """ All Instance Related Functions """
    allowed_instances: PlatformInstances

    def get_instance_type(self, gpu_type: GPUType, gpu_num: int, cpus: Optional[int] = None) -> InstanceType:
        return self.allowed_instances.get_instance_type(
            gpu_type=gpu_type,
            gpu_num=gpu_num,
            cpus=cpus,
        )


class PlatformPriorityHandler():
    # priority class to use for the job
    priority_class_labels: Dict[str, str] = {}
    default_priority_class: Optional[str] = None  # If a priority class should be default, put it here.

    def get_priority_class_label(self, priority_class_override: Optional[str]) -> Optional[str]:
        priority_class = priority_class_override if priority_class_override else self.default_priority_class
        priority_class_label: Optional[str] = None
        if priority_class is not None:
            if priority_class not in self.priority_class_labels:
                raise ValueError(
                    f'Invalid priority class. Must be one of {self.priority_class_labels}, not {priority_class}')
            priority_class_label = self.priority_class_labels[priority_class]
        return priority_class_label


class PlatformProperties():
    mcli_platform: MCLIPlatform

    @property
    def namespace(self):
        return self.mcli_platform.namespace

    @property
    def kubernetes_context(self):
        return self.mcli_platform.kubernetes_context


class GenericK8sPlatform(
        PlatformResourceHandler,
        PlatformPriorityHandler,
        PlatformProperties,
        PlatformExperimental,
):
    """ A Generic Platform implementation """

    interactive: bool = False
    pod_group_scheduler: Optional[str] = None

    @classmethod
    def from_mcli_platform(cls, mcli_platform: MCLIPlatform) -> GenericK8sPlatform:
        # pylint: disable-next=import-outside-toplevel
        from mcli.serverside.platforms.overrides import (AWSPlatform, AzurePlatform, COTAPlatform, GCPPlatform,
                                                         R1Z1Platform, R1Z2Platform, R6Z1Platform, R6Z2Platform)

        # pylint: disable-next=invalid-name
        K8S_CONTEXT_PLATFORM_MAP: Dict[str, Type[GenericK8sPlatform]] = {
            'aws-research-01': AWSPlatform,
            'azure-research-01': AzurePlatform,
            'gcp-research-01': GCPPlatform,
            'colo-research-01': COTAPlatform,
            'r1z1': R1Z1Platform,
            'r1z2': R1Z2Platform,
            'r6z1': R6Z1Platform,
            'r6z2': R6Z2Platform,
        }
        if mcli_platform.kubernetes_context not in K8S_CONTEXT_PLATFORM_MAP:
            raise PlatformCreationError()
        k8s_platform = K8S_CONTEXT_PLATFORM_MAP[mcli_platform.kubernetes_context]
        return k8s_platform(mcli_platform=mcli_platform)

    def __init__(self, mcli_platform: MCLIPlatform) -> None:
        self.mcli_platform = mcli_platform
        self.secret_manager = SecretManager(mcli_platform=mcli_platform)
        self.interactive = False
        super().__init__()

    def setup(self) -> bool:
        """Setup the platform for future use.

        This method should be implemented by any platform that requires user-specific setup to be performed on
        MCLIPlatform creation. This should be idempotent, such that if the setup is already completed, this should be
        a no-op.

        Raises:
            PlatformSetupError: Raised if setup failure prevents use of the platform
        """
        return True

    def get_annotations(self, instance_type: InstanceType):
        del instance_type
        return {}

    def get_volumes(self) -> List[MCLIVolume]:
        return [
            MCLIVolume(
                volume=client.V1Volume(
                    name='dshm',
                    empty_dir=client.V1EmptyDirVolumeSource(medium='Memory'),
                ),
                volume_mount=client.V1VolumeMount(
                    name='dshm',
                    mount_path='/dev/shm',
                ),
            ),
        ]

    def get_tolerations(self, instance_type: InstanceType) -> List[Dict[str, str]]:
        del instance_type
        return []

    def prepare_kubernetes_job_for_platform(
        self,
        kubernetes_job: MCLIK8sJob,
        instance_type: InstanceType,
        priority_class: Optional[str] = None,
        experimental_flags: Optional[List[ExperimentalFlag]] = None,
    ) -> None:
        """Modifies a MCLIK8sJob with the proper specs of the Platform

        Args:
            kubernetes_job: The MCLIK8sJob object to that represents the K8s job
            instance_type: The instance type to use on the platform
            priority_class: An optional priority class to assign the job to
        """
        kubernetes_job.metadata.namespace = self.namespace
        kubernetes_job.spec.backoff_limit = 0

        resources = instance_type.resource_requirements
        kubernetes_job.container.resources = resources

        volumes = self.get_volumes()
        for volume in volumes:
            kubernetes_job.add_volume(volume)

        pod_spec = kubernetes_job.pod_spec
        pod_spec.priority_class_name = self.get_priority_class_label(priority_class_override=priority_class)

        pod_spec.restart_policy = 'Never'
        pod_spec.host_ipc = True

        self.apply_experimental_flags(
            kubernetes_job=kubernetes_job,
            platform_instance=self.allowed_instances,
            instance_type=instance_type,
            experimental_flags=experimental_flags,
        )

        # Add secrets to job
        self.secret_manager.add_secrets_to_job(kubernetes_job=kubernetes_job)
