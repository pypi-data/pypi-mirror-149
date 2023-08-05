# pylint: disable=duplicate-code

""" R6Z2 Platform Definition """
from typing import Dict, Optional

from mcli.serverside.platforms.instance_type import InstanceList
from mcli.serverside.platforms.overrides.r6z2_instances import R6Z2_INSTANCE_LIST
from mcli.serverside.platforms.platform import GenericK8sPlatform

NUM_MULTI_GPU_TOLERATE = 8
MAX_CPUS = 60

R6Z2_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'scavenge': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'emergency': 'mosaicml-internal-research-emergency-priority'
}


class R6Z2Platform(GenericK8sPlatform):
    """ R6Z2 Platform Overrides """

    HOST_MEMORY_PER_GPU_GB: int = 230
    allowed_instances: InstanceList = R6Z2_INSTANCE_LIST
    priority_class_labels = R6Z2_PRIORITY_CLASS_LABELS  # type: Dict[str, str]
    default_priority_class: str = 'standard'
    pod_group_scheduler: Optional[str] = 'scheduler-plugins-scheduler'
