# pylint: disable=duplicate-code

""" The GCP Platform """

from mcli.serverside.platforms.overrides.gcp_instances import GCP_ALLOWED_INSTANCES
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import PlatformInstances


class GCPPlatform(GenericK8sPlatform):
    """ The GCP Platform """

    allowed_instances: PlatformInstances = GCP_ALLOWED_INSTANCES
