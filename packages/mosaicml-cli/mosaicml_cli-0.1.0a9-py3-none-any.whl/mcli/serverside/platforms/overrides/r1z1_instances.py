# pylint: disable=duplicate-code

""" Available Instances for the R1Z1 Platform """

from typing import List

from mcli.serverside.platforms.instance_type import GPUType, InstanceList, InstanceType
from mcli.utils.utils_kube_labels import label

DEFAULT_CPUS_PER_GPU = 7
n = DEFAULT_CPUS_PER_GPU  # shorthand for below

ALLOWED_INSTANCES = [
    InstanceType(
        name='r1z1-g0',
        cpu_count=1,
        gpu_count=0,
        gpu_type=GPUType.A100,
        desc='Single cpu pod',
    ),
    InstanceType(
        name='r1z1-g1-a100',
        cpu_count=n * 1,
        gpu_count=1,
        gpu_type=GPUType.A100,
        gpu_memory=80,
        desc='1x a100s',
    ),
    InstanceType(
        name='r1z1-g2-a100',
        cpu_count=n * 2,
        gpu_count=2,
        gpu_type=GPUType.A100,
        gpu_memory=80,
        desc='2x a100s',
    ),
    InstanceType(
        name='r1z1-g4-a100',
        cpu_count=n * 4,
        gpu_count=4,
        gpu_type=GPUType.A100,
        gpu_memory=80,
        desc='4x a100s',
    ),
    InstanceType(
        name='r1z1-g8-a100',
        cpu_count=n * 8,
        gpu_count=8,
        gpu_type=GPUType.A100,
        gpu_memory=80,
        desc='8x a100s',
    ),
]


class R1Z1InstanceList(InstanceList):
    """ Available Instances for the R1Z1 Platform """

    def add_node_selector_to_instance(self, instance: InstanceType) -> None:
        instance.extras.update({'node_selector': label.mosaic.cloud.INSTANCE_SIZE})

        if instance.gpu_type == GPUType.A100:
            instance.extras.update({'node_class': label.mosaic.instance_size_types.A100_80G_1})

    def __init__(self, instances: List[InstanceType]) -> None:
        for r1z1_instance in instances:
            self.add_node_selector_to_instance(r1z1_instance)
        super().__init__(instances=instances)


R1Z1_INSTANCE_LIST = R1Z1InstanceList(instances=ALLOWED_INSTANCES)
