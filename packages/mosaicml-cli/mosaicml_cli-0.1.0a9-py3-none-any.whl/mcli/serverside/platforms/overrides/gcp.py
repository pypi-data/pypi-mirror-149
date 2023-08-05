# pylint: disable=duplicate-code

""" The GCP Platform """

from mcli.serverside.platforms.instance_type import InstanceList
from mcli.serverside.platforms.overrides.gcp_instances import GCP_INSTANCE_LIST
from mcli.serverside.platforms.platform import GenericK8sPlatform


class GCPPlatform(GenericK8sPlatform):
    """ The GCP Platform """

    allowed_instances: InstanceList = GCP_INSTANCE_LIST
