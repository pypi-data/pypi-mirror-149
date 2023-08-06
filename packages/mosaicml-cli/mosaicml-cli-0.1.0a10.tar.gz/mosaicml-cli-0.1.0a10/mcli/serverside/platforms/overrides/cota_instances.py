# pylint: disable=duplicate-code

""" The InstanceList of allowed COTA InstanceTypes """

from typing import List

from mcli.serverside.platforms.instance_type import GPUType, InstanceList, InstanceType
from mcli.utils.utils_kube_labels import label

DEFAULT_CPUS_PER_GPU = 15
n = DEFAULT_CPUS_PER_GPU  # shorthand for below
NUM_MULTI_GPU_TOLERATE = 8

ALLOWED_INSTANCES = [
    InstanceType(
        name='cota-c1',
        cpu_count=1,
        gpu_count=0,
        desc='1 cpus',
    ),
    InstanceType(
        name='cota-c20',
        cpu_count=20,
        gpu_count=0,
        desc='20 cpus',
    ),
    InstanceType(
        name='cota-g1-3080',
        cpu_count=n * 1,
        gpu_count=1,
        gpu_type=GPUType.RTX3080,
        gpu_memory=10,
        desc='1x 3080s',
    ),
    InstanceType(
        name='cota-g2-3080',
        cpu_count=n * 2,
        gpu_count=2,
        gpu_type=GPUType.RTX3080,
        gpu_memory=10,
        desc='2x 3080s',
    ),
    InstanceType(
        name='cota-g4-3080',
        cpu_count=n * 4,
        gpu_count=4,
        gpu_type=GPUType.RTX3080,
        gpu_memory=10,
        desc='4x 3080s',
    ),
    InstanceType(
        name='cota-g8-3080',
        cpu_count=n * 8,
        gpu_count=8,
        gpu_type=GPUType.RTX3080,
        gpu_memory=10,
        desc='8x 3080s',
    ),
    InstanceType(
        name='cota-g1-3090',
        cpu_count=n * 1,
        gpu_count=1,
        gpu_type=GPUType.RTX3090,
        gpu_memory=24,
        desc='1x 3090s',
    ),
    InstanceType(
        name='cota-g2-3090',
        cpu_count=n * 2,
        gpu_count=2,
        gpu_type=GPUType.RTX3090,
        gpu_memory=24,
        desc='2x 3090s',
    ),
    InstanceType(
        name='cota-g4-3090',
        cpu_count=n * 4,
        gpu_count=4,
        gpu_type=GPUType.RTX3090,
        gpu_memory=24,
        desc='4x 3090s',
    ),
    InstanceType(
        name='cota-g8-3090',
        cpu_count=n * 8,
        gpu_count=8,
        gpu_type=GPUType.RTX3090,
        gpu_memory=24,
        desc='8x 3090s',
    ),
]


class CotaInstanceList(InstanceList):
    """ The Cota Instance List with Custom Naming Schema """

    def add_node_selector_to_instance(self, instance: InstanceType) -> None:
        instance.extras.update({'node_selector': label.mosaic.NODE_CLASS})

        if instance.gpu_type == GPUType.RTX3080:
            instance.extras.update({'node_class': 'mml-nv3080'})
        elif instance.gpu_type == GPUType.RTX3090:
            instance.extras.update({'node_class': 'mml-nv3090'})

        if instance.gpu_count == NUM_MULTI_GPU_TOLERATE:
            instance.extras.update({label.mosaic.cota.MULTIGPU_8: 'true'})

    def __init__(self, instances: List[InstanceType]) -> None:

        for cota_instance in instances:
            self.add_node_selector_to_instance(cota_instance)
        super().__init__(instances=instances)


COTA_INSTANCE_LIST = CotaInstanceList(instances=ALLOWED_INSTANCES)
