# pylint: disable=duplicate-code

""" A Singleton Platform Registry for all Sub Platforms """
from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Type

from mcli import config
from mcli.models import MCLIPlatform
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.overrides import (AWSPlatform, AzurePlatform, COTAPlatform, GCPPlatform, R1Z1Platform,
                                                 R1Z2Platform, R6Z1Platform, R6Z2Platform)
from mcli.serverside.platforms.platform import GenericK8sPlatform

k8s_platforms: Dict[str, Type[GenericK8sPlatform]] = {
    'aws-research-01': AWSPlatform,
    'azure-research-01': AzurePlatform,
    'gcp-research-01': GCPPlatform,
    'colo-research-01': COTAPlatform,
    'r1z1': R1Z1Platform,
    'r1z2': R1Z2Platform,
    'r6z1': R6Z1Platform,
    'r6z2': R6Z2Platform,
}


class PlatformRegistry():
    """ A Singleton designed to track multiple platforms """

    def __init__(self):
        self._platforms = {}
        self._instance_lookup = {}

    @property
    def platforms(self) -> List[MCLIPlatform]:
        return config.get_mcli_config().platforms

    def get(self, platform_name: str) -> GenericK8sPlatform:
        """ Returns platform by name """
        if platform_name not in self._platforms:
            raise ValueError(f'No such platform: {platform_name}')
        else:
            return self._platforms[platform_name]

    def get_k8s_platform(self, platform: MCLIPlatform) -> GenericK8sPlatform:
        if platform.kubernetes_context in k8s_platforms:
            found_platform = k8s_platforms[platform.kubernetes_context]
            return found_platform(platform_information=platform)
        return GenericK8sPlatform(platform_information=platform)

    def get_mcli_platform_and_instance_type(self, instance_str: str) -> Tuple[MCLIPlatform, InstanceType]:
        """ This method is a hack.  Returns both MCLIPlatform and InstanceType from a instance_str
        TODO(HEK-323)
        """
        possible_platforms: List[Tuple[MCLIPlatform, InstanceType]] = []
        for platform in self.platforms:
            found_k8s_platforms = self.get_k8s_platform(platform)
            try:
                instance_type = found_k8s_platforms.get_instance(instance_str)
                possible_platforms.append((
                    platform,
                    instance_type,
                ))
            except Exception as _:  # pylint: disable=broad-except
                pass
        if len(possible_platforms) == 0:
            raise ValueError(f'Unable to find a platform to run instance {instance_str} on')
        if len(possible_platforms) > 1:
            platforms_found_str = ','.join([x.name for x, _ in possible_platforms])
            print(f'WARNING: Multiple possible execution platforms found: {platforms_found_str}'
                  f'\nDefaulting to {possible_platforms[0][0].name}')
        return possible_platforms[0]

    def get_for_instance_type(self, instance_type: InstanceType) -> GenericK8sPlatform:
        """ Returns platform by instance type """
        found_platform: Optional[GenericK8sPlatform] = None

        for platform in self.platforms:
            k8s_platform = self.get_k8s_platform(platform)
            if k8s_platform.is_allowed_instance(instance_type):

                # check for duplicate allowed instances
                if found_platform is not None:
                    raise ValueError(f'{instance_type} found on multiple' + f'platforms: {found_platform}, {platform}.')
                else:
                    found_platform = k8s_platform

        if found_platform is None:
            raise ValueError(f'Instance type {instance_type} not in allowed instances.')
        else:
            return found_platform
