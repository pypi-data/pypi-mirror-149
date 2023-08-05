# pylint: disable=duplicate-code

""" The Azure Platform """

from mcli.serverside.platforms.instance_type import InstanceList
from mcli.serverside.platforms.overrides.azure_instances import AZURE_INSTANCE_LIST
from mcli.serverside.platforms.platform import GenericK8sPlatform


class AzurePlatform(GenericK8sPlatform):
    """ The Azure Platform """

    allowed_instances: InstanceList = AZURE_INSTANCE_LIST
