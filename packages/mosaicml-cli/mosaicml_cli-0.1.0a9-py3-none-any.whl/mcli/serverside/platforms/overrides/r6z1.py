# pylint: disable=duplicate-code

""" R1Z6 Platform Definition """
from typing import Dict

from mcli.serverside.platforms.instance_type import InstanceList
from mcli.serverside.platforms.overrides.r6z1_instances import R6Z1_INSTANCE_LIST
from mcli.serverside.platforms.platform import GenericK8sPlatform

MAX_CPUS = 60

R6Z1_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'scavenge': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'emergency': 'mosaicml-internal-research-emergency-priority'
}


class R6Z1Platform(GenericK8sPlatform):
    """ R6Z1 Platform Overrides """

    HOST_MEMORY_PER_GPU_GB: int = 230
    allowed_instances: InstanceList = R6Z1_INSTANCE_LIST
    priority_class_labels = R6Z1_PRIORITY_CLASS_LABELS  # type: Dict[str, str]
    default_priority_class: str = 'standard'
