""" Available Instances for the R6Z1 Platform """

from typing import List

from mcli.serverside.platforms.experimental import ExperimentalFlag
from mcli.serverside.platforms.instance_type import GPUType, InstanceList, InstanceType
from mcli.utils.utils_kube_labels import label

DEFAULT_CPUS_PER_GPU = 7
n = DEFAULT_CPUS_PER_GPU  # shorthand for below

ALLOWED_INSTANCES = [
    InstanceType(
        name='r6z1-g1-a100',
        cpu_count=n * 1,
        gpu_count=1,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='1x a100s',
    ),
    InstanceType(
        name='r6z1-g2-a100',
        cpu_count=n * 2,
        gpu_count=2,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='2x a100s',
    ),
    InstanceType(
        name='r6z1-g4-a100',
        cpu_count=n * 4,
        gpu_count=4,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='4x a100s',
    ),
    InstanceType(
        name='r6z1-g8-a100',
        cpu_count=n * 8,
        gpu_count=8,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='8x a100s',
    ),
]


class R6Z1InstanceList(InstanceList):
    """ Available Instances for the R6Z1 Platform """

    def add_node_selector_to_instance(self, instance: InstanceType) -> None:
        instance.extras.update({'node_selector': label.mosaic.cloud.INSTANCE_SIZE})

        if instance.gpu_type == GPUType.A100:
            instance.extras.update({'node_class': label.mosaic.instance_size_types.OCI_G4_8})

    def add_experimental_flags_to_instance(self, instance: InstanceType) -> None:
        """Adds available experimental flags to each applicable instance

        Args:
            instance (InstanceType): Instance to add flags to
        """
        if instance.gpu_count == 8:
            instance.extras.setdefault('experimental', []).append(ExperimentalFlag.RDMA)

    def __init__(self, instances: List[InstanceType]) -> None:

        for r6z1_instance in instances:
            self.add_node_selector_to_instance(r6z1_instance)
            self.add_experimental_flags_to_instance(r6z1_instance)
        super().__init__(instances=instances)


R6Z1_INSTANCE_LIST = R6Z1InstanceList(instances=ALLOWED_INSTANCES)
