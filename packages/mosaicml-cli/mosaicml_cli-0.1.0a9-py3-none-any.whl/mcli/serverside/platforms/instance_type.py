# pylint: disable=duplicate-code

""" The InstanceType Abstraction for different instance configs """
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional, Set

import yaml
from kubernetes import client

from mcli.utils.utils_kube_labels import label


class GPUType(Enum):
    """ The Type of GPU to use in a job """
    NONE = 'none'
    A100 = 'A100'
    V100 = 'V100'
    P100 = 'P100'
    T4 = 'T4'
    K80 = 'K80'
    RTX3080 = '3080'
    RTX3090 = '3090'
    TPUv2 = 'TPUv2'  # pylint: disable=invalid-name
    TPUv3 = 'TPUv3'  # pylint: disable=invalid-name


@dataclass
class InstanceType():
    """ The InstanceType Abstraction for different instance configs """
    name: str
    desc: str
    cpu_count: int
    gpu_count: Optional[int]
    gpu_type: GPUType = GPUType.NONE
    gpu_memory: Optional[int] = None
    extras: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        data = asdict(self)
        data['gpu_type'] = data['gpu_type'].value
        return yaml.dump(data)

    def __gt__(self, other):
        return self.name < other.name

    @property
    def node_class(self) -> str:
        """ Retrieves the node_class if set in extras,
        otherwise falls back to instance_type.name
        """
        return self.extras.get('node_class', self.name)

    @property
    def node_selectors(self) -> Dict[str, str]:
        """ Retrieves the node_selectors if set in extras,
        otherwise falls back to K8s Default selector
        """
        selectors = {}
        node_class = self.node_class
        instance_type_selector = self.extras.get('node_selector', label.kubernetes_node.INSTANCE_TYPE)
        selectors.update({instance_type_selector: node_class})
        extra_selectors = self.extras.get('selectors', {})
        selectors.update(extra_selectors)
        return selectors

    @property
    def is_gpu(self) -> bool:
        return self.gpu_count is not None and self.gpu_count > 0

    @property
    def resource_requirements(self) -> client.V1ResourceRequirements:
        """
        Returns resource requests and limits for kubernetes
        """
        requests: Dict[str, int] = {}
        limits: Dict[str, int] = {}
        if self.gpu_count is not None and self.gpu_count > 0:
            limits[label.nvidia.GPU] = self.gpu_count

        # -1 core for buffer
        requests['cpu'] = self.cpu_count - 1 if self.cpu_count > 1 else self.cpu_count
        limits['cpu'] = self.cpu_count

        return client.V1ResourceRequirements(
            requests=requests,
            limits=limits,
        )


class InstanceList():
    """ An abstraction over a platforms available instance types """

    def __init__(self, instances: List[InstanceType]) -> None:
        self.instances = instances

    def get_allowed_instances(self) -> Set[str]:
        return {i.name for i in self.instances}

    def get_instance_by_name(self, instance_name: str) -> Optional[InstanceType]:
        for inst in self.instances:
            if inst.name == instance_name:
                return inst
        return None

    def is_allowed_instance_type(self, instance_type: InstanceType) -> bool:
        for inst in self.instances:
            if inst.name == instance_type.name:
                return True
        return False

    def __iter__(self) -> Iterator[InstanceType]:
        """ allow iteration through the instances"""
        return iter(self.instances)
