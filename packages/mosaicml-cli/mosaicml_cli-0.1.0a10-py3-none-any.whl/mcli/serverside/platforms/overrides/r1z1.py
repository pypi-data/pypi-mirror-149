# pylint: disable=duplicate-code

""" R1Z1 Platform Definition """
from typing import Dict, List

from kubernetes import client

from mcli import config
from mcli.serverside.job.mcli_k8s_job import MCLIVolume
from mcli.serverside.platforms.instance_type import InstanceList
from mcli.serverside.platforms.overrides.r1z1_instances import R1Z1_INSTANCE_LIST
from mcli.serverside.platforms.platform import GenericK8sPlatform

MAX_CPUS = 60

R1Z1_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'scavenge': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'emergency': 'mosaicml-internal-research-emergency-priority'
}


class R1Z1Platform(GenericK8sPlatform):
    """ R1Z1 Platform Overrides """

    allowed_instances: InstanceList = R1Z1_INSTANCE_LIST
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
