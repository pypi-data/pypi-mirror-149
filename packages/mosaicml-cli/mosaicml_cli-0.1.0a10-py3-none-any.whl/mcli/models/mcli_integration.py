""" Implements MCLI Integrations """
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, Optional, Type, Union

import yaml

from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob
from mcli.utils.utils_serializable_dataclass import SerializableDataclass, T_SerializableDataclass


class IntegrationType(Enum):
    """ Enum for Types of Setup Items Allowed """
    wandb = 'wandb'
    git_repo = 'git_repo'
    apt_packages = 'apt_packages'
    pip_packages = 'pip_packages'

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def ensure_enum(cls, val: Union[str, IntegrationType]) -> IntegrationType:
        if isinstance(val, str):
            return IntegrationType[val]
        elif isinstance(val, IntegrationType):
            return val
        raise ValueError(f'Unable to ensure {val} is a SetupItemType Enum')


@dataclass
class MCLIIntegration(SerializableDataclass, ABC):
    """
    The Base Integration Class for MCLI SetupItems

    SetupItems can not nest other SerializableDataclass objects
    """

    integration_type: IntegrationType

    @abstractmethod
    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        """Add a integration to a job
        """

    @classmethod
    def from_dict(cls: Type[T_SerializableDataclass], data: Dict[str, Any]) -> T_SerializableDataclass:
        integration_type = data.get('integration_type', None)
        if not integration_type:
            raise ValueError(f'No `integration_type` found for integration with data: \n{yaml.dump(data)}')

        integration_type: IntegrationType = IntegrationType.ensure_enum(integration_type)
        data['integration_type'] = integration_type

        # pylint: disable-next=import-outside-toplevel
        from mcli.objects.integrations import (MCLIAptPackagesIntegration, MCLIGitRepoIntegration,
                                               MCLIPipPackagesIntegration, MCLIWanDBIntegration)
        integration: Optional[MCLIIntegration] = None
        if integration_type == IntegrationType.wandb:
            integration = MCLIWanDBIntegration(**data)
        elif integration_type == IntegrationType.git_repo:
            integration = MCLIGitRepoIntegration(**data)
        elif integration_type == IntegrationType.apt_packages:
            integration = MCLIAptPackagesIntegration(**data)
        elif integration_type == IntegrationType.pip_packages:
            integration = MCLIPipPackagesIntegration(**data)
        else:
            raise NotImplementedError(f'Setup Item of type: { integration_type } not supported yet')
        assert isinstance(integration, MCLIIntegration)
        return integration  # type: ignore

    def __str__(self) -> str:
        data = asdict(self)
        del data['integration_type']
        return f'Integration: {self.integration_type.value}' + f'\n{ yaml.dump( data ) }'
