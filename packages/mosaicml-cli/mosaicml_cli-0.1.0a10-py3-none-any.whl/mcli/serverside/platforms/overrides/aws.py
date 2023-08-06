# pylint: disable=duplicate-code

""" The AWS Platform """

from mcli.serverside.platforms.instance_type import InstanceList
from mcli.serverside.platforms.overrides.aws_instances import AWS_INSTANCE_LIST
from mcli.serverside.platforms.platform import GenericK8sPlatform


class AWSPlatform(GenericK8sPlatform):
    """ The AWS Platform """

    allowed_instances: InstanceList = AWS_INSTANCE_LIST
