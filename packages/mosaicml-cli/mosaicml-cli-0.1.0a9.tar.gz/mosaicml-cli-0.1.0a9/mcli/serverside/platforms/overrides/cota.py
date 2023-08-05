# pylint: disable=duplicate-code

""" The COTA Platform """
from typing import Dict, List

from kubernetes import client

from mcli.serverside.job.mcli_job import MCLIVolume
from mcli.serverside.platforms.instance_type import InstanceList, InstanceType
from mcli.serverside.platforms.overrides.cota_instances import COTA_INSTANCE_LIST, NUM_MULTI_GPU_TOLERATE
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.utils.utils_kube_labels import label


class COTAPlatform(GenericK8sPlatform):
    """ The COTA Platform """

    allowed_instances: InstanceList = COTA_INSTANCE_LIST

    def get_volumes(self) -> List[MCLIVolume]:
        volumes = super().get_volumes()
        volumes.append(
            MCLIVolume(
                volume=client.V1Volume(
                    name='local',
                    host_path=client.V1HostPathVolumeSource(path='/localdisk', type='Directory'),
                ),
                volume_mount=client.V1VolumeMount(
                    name='local',
                    mount_path='/localdisk',
                ),
            ))

        return volumes

    def get_tolerations(self, instance_type: InstanceType) -> List[Dict[str, str]]:
        tolerations = []
        resources = instance_type.resource_requirements
        num_gpus = 0
        if isinstance(resources.limits, dict):
            num_gpus = resources.limits.get(label.nvidia.GPU, 0)

        if num_gpus > 0:
            tolerations.append({
                'effect': 'PreferNoSchedule',
                'key': label.mosaic.cota.PREFER_GPU_WORKLOADS,
                'operator': 'Equal',
                'value': 'true'
            })

        if num_gpus == NUM_MULTI_GPU_TOLERATE:
            tolerations.append({
                'effect': 'NoSchedule',
                'key': label.mosaic.cota.MULTIGPU_8,
                'operator': 'Equal',
                'value': 'true'
            })

        return tolerations
