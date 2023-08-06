# pylint: disable=duplicate-code

""" The base class for how a platform will operate """

from abc import ABC
from typing import Any, Dict, List, Optional, Set

from kubernetes import client

from mcli.models import MCLIPlatform
from mcli.objects.secrets.platform_secret import SecretManager
from mcli.serverside.job.mcli_job import MCLIK8sJob, MCLIVolume
from mcli.serverside.platforms.experimental import ExperimentalFlag, PlatformExperimental
from mcli.serverside.platforms.instance_type import InstanceList, InstanceType
from mcli.utils.utils_kube import safe_update_optional_dictionary, safe_update_optional_list
from mcli.utils.utils_kube_labels import label

# types
Resources = Dict[str, int]
Description = Dict[str, Any]


class PlatformSetupError(Exception):
    """Raised if platform setup failed
    """


class PlatformInstance(ABC):
    """ All Instance Related Functions """
    allowed_instances: InstanceList  # InstanceList

    def is_allowed_instance(self, instance_type: InstanceType) -> bool:
        """ checks if the instance type is an allowed instances """
        return self.allowed_instances.is_allowed_instance_type(instance_type=instance_type)

    def get_instance(self, instance_type: str) -> InstanceType:
        """ gets the InstanceType from a str, throws if not available in platform"""
        instance = self.allowed_instances.get_instance_by_name(instance_name=instance_type)
        if instance is None:
            raise ValueError(f'{instance_type} not found in {self.__class__.__name__}')
        assert isinstance(instance, InstanceType)
        return instance

    # All Interactive Related Functions
    interactive: bool = False

    def get_allowed_interactive_gpu_nums(self,) -> Set[int]:
        if not self.interactive:
            return set()
        num_gpus = {x.gpu_count for x in self.allowed_instances if x.gpu_count is not None}
        if 0 in num_gpus:
            num_gpus.remove(0)
        if num_gpus == 0:
            raise ValueError('For now 0 GPU instances are not allowed')
        return num_gpus

    def get_interactive_instance_from_gpus(self, num_gpus: int) -> Optional[InstanceType]:
        """ gets the InstanceType from a number of gpus for an interactive platform """
        if not self.interactive:
            return None
        if num_gpus == 0:
            raise ValueError('For now 0 GPU instances are not allowed')
        for instance in self.allowed_instances:
            if instance.gpu_count == num_gpus:
                return instance
        return None


class PlatformPriority(ABC):
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


class PlatformResources():
    """ Resources like Ram and Storage for jobs on a platform basis """

    HOST_MEMORY_PER_GPU_GB: int = 58
    HOST_EPHEMERAL_STORAGE_PER_GPU_GB: int = 200

    def add_platform_resources(
        self,
        resources: client.V1ResourceRequirements,
        num_gpus: float,
    ):
        if num_gpus == 0:
            # TODO: Hack for 0 gpu workflows
            num_gpus = 0.1
        total_memory = num_gpus * self.HOST_MEMORY_PER_GPU_GB
        total_storage = num_gpus * self.HOST_EPHEMERAL_STORAGE_PER_GPU_GB
        if not isinstance(resources.limits, dict):
            resources.limits = {}
        if not isinstance(resources.requests, dict):
            resources.requests = {}
        resources.limits['memory'] = f'{total_memory}G'
        resources.requests['memory'] = f'{total_memory}G'
        resources.limits['ephemeral-storage'] = f'{total_storage}G'
        resources.requests['ephemeral-storage'] = f'{total_storage}G'


class PlatformProperties(ABC):
    platform_information: MCLIPlatform

    @property
    def namespace(self):
        return self.platform_information.namespace


class GenericK8sPlatform(
        PlatformInstance,
        PlatformPriority,
        PlatformResources,
        PlatformProperties,
        PlatformExperimental,
):
    """ A Generic Platform implementation """

    pod_group_scheduler: Optional[str] = None

    def __init__(self, platform_information: MCLIPlatform) -> None:
        self.platform_information = platform_information
        self.secret_manager = SecretManager(platform_information)
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

    def get_node_selectors(self, instance_type: InstanceType) -> Dict[str, str]:
        # Possibly add multi-node selectors here
        return instance_type.node_selectors

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
            experimental_flags: A list of experimental flags to enable,
                if the instance allows them. Defaults to None.
        """
        if experimental_flags is None:
            experimental_flags = []

        kubernetes_job.metadata.namespace = self.namespace
        kubernetes_job.spec.backoff_limit = 0

        env_vars = {'MOSAICML_INSTANCE_TYPE': instance_type.name}

        resources = instance_type.resource_requirements
        kubernetes_job.container.resources = resources

        num_gpus = 0
        if isinstance(resources.limits, dict):
            num_gpus = resources.limits.get(label.nvidia.GPU, 0)

        if num_gpus == 0:
            # If no GPUs requested, limit the container visibility with this envvar.
            # see: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/user-guide.html#gpu-enumeration
            env_vars['NVIDIA_VISIBLE_DEVICES'] = 'void'  # type: ignore

        self.add_platform_resources(resources=resources, num_gpus=num_gpus)

        volumes = self.get_volumes()
        for volume in volumes:
            kubernetes_job.add_volume(volume)

        pod_spec = kubernetes_job.pod_spec
        pod_spec.priority_class_name = self.get_priority_class_label(priority_class_override=priority_class)
        for env_name, env_value in env_vars.items():
            kubernetes_job.add_env_var(client.V1EnvVar(
                name=env_name,
                value=env_value,
            ))

        pod_spec.restart_policy = 'Never'
        pod_spec.host_ipc = True
        pod_spec.tolerations = safe_update_optional_list(
            pod_spec.tolerations,
            self.get_tolerations(instance_type),
        )
        pod_spec.node_selector = safe_update_optional_dictionary(
            pod_spec.node_selector,
            self.get_node_selectors(instance_type),
        )

        # Apply optional experimental flags
        self.apply_experimental_flags(
            kubernetes_job=kubernetes_job,
            instance=instance_type,
            experimental_flags=experimental_flags,
        )

        # Add secrets to job
        self.secret_manager.add_secrets_to_job(kubernetes_job=kubernetes_job)

    def get_shared_metadata(self, instance_type: InstanceType) -> client.V1ObjectMeta:
        return client.V1ObjectMeta(
            namespace=self.namespace,
            labels={
                label.mosaic.LABEL_INSTANCE: instance_type.name,
            },
        )
