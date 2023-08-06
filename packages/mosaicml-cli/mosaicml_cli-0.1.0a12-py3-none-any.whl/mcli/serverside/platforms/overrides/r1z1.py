""" R1Z1 Platform Definition """
from typing import Dict, List

from kubernetes import client

from mcli import config
from mcli.serverside.job.mcli_k8s_job import MCLIVolume
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import (LocalPlatformInstances, PlatformInstanceGPUConfiguration,
                                                          PlatformInstances)
from mcli.utils.utils_kube_labels import label

MAX_CPUS = 60

R1Z1_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'scavenge': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'emergency': 'mosaicml-internal-research-emergency-priority'
}

a100_config = PlatformInstanceGPUConfiguration(
    gpu_type=GPUType.A100_80GB,
    gpu_nums=[1, 2, 4, 8],
    gpu_selectors={label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.A100_80G_1},
    cpus=64,
    cpus_per_gpu=8,
    memory=512,
    memory_per_gpu=64,
    storage=1600,
    storage_per_gpu=200,
)

R1Z1_INSTANCES = LocalPlatformInstances(gpu_configurations=[a100_config])


class R1Z1Platform(GenericK8sPlatform):
    """ R1Z1 Platform Overrides """

    allowed_instances: PlatformInstances = R1Z1_INSTANCES
    priority_class_labels = R1Z1_PRIORITY_CLASS_LABELS  # type: Dict[str, str]
    default_priority_class: str = 'standard'

    def get_volumes(self) -> List[MCLIVolume]:
        volumes = super().get_volumes()
        mcli_config = config.MCLIConfig.load_config()
        if mcli_config.feature_enabled(feature=config.FeatureFlag.USE_LOCALDISK_FOR_MATTHEW_ONLY):
            volumes.append(
                MCLIVolume(
                    volume=client.V1Volume(
                        name='local',
                        host_path=client.V1HostPathVolumeSource(path='/localdisk', type='Directory'),
                    ),
                    volume_mount=client.V1VolumeMount(
                        name='local',
                        mount_path='/localdisk',
                        read_only=True,
                    ),
                ))
        return volumes
