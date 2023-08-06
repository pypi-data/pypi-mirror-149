""" The AWS Platform """

from mcli.serverside.platforms import PlatformInstances
from mcli.serverside.platforms.overrides.aws_instances import AWS_ALLOWED_INSTANCES
from mcli.serverside.platforms.platform import GenericK8sPlatform


class AWSPlatform(GenericK8sPlatform):
    """ The AWS Platform """

    allowed_instances: PlatformInstances = AWS_ALLOWED_INSTANCES
