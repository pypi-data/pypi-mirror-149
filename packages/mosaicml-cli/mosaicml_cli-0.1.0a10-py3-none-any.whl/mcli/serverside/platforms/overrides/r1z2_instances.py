# pylint: disable=duplicate-code

""" Available Instances for the R1Z1 Platform """
from typing import List

from mcli.serverside.platforms.instance_type import GPUType, InstanceList, InstanceType
from mcli.utils.utils_kube_labels import label

DEFAULT_CPUS_PER_GPU = 7
n = DEFAULT_CPUS_PER_GPU  # shorthand for below

ALLOWED_INSTANCES = [
    InstanceType(
        name='r1z2-g1-a100',
        cpu_count=n * 1,
        gpu_count=1,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='1x a100s',
    ),
    InstanceType(
        name='r1z2-g2-a100',
        cpu_count=n * 2,
        gpu_count=2,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='2x a100s',
    ),
    InstanceType(
        name='r1z2-g4-a100',
        cpu_count=n * 4,
        gpu_count=4,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='4x a100s',
    ),
]


class R1Z2InstanceList(InstanceList):
    """ Available Instances for the R1Z2 Platform """

    def add_node_selector_to_instance(self, instance: InstanceType) -> None:
        instance.extras.update({'node_selector': label.mosaic.cloud.INSTANCE_SIZE})

        if instance.gpu_type == GPUType.A100:
            instance.extras.update({'node_class': label.mosaic.instance_size_types.A100_40G_1})

    def __init__(self, instances: List[InstanceType]) -> None:
        for r1z1_instance in instances:
            self.add_node_selector_to_instance(r1z1_instance)
        super().__init__(instances=instances)


R1Z2_INSTANCE_LIST = R1Z2InstanceList(instances=ALLOWED_INSTANCES)
