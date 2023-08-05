""" MCLI Abstraction for Platforms """
from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Generator, List

from mcli.models.mcli_envvar import MCLIEnvVar
from mcli.utils.utils_kube import KubeContext, use_context
from mcli.utils.utils_serializable_dataclass import SerializableDataclass

logger = logging.getLogger(__name__)


@dataclass
class MCLIPlatform(SerializableDataclass):
    """Configured MCLI platform relating to specific kubernetes context
    """
    name: str
    kubernetes_context: str
    namespace: str
    environment_overrides: List[MCLIEnvVar] = field(default_factory=list)

    @classmethod
    @contextmanager
    def use(cls, platform: MCLIPlatform) -> Generator[MCLIPlatform, None, None]:
        """Temporarily set the platform to use for all Kubernetes API calls

        Args:
            platform (MCLIPlatform): The platform to use

        Yields:
            MCLIPlatform: The provided platform
        """
        with use_context(platform.kubernetes_context):
            yield platform

    def to_kube_context(self) -> KubeContext:
        """Get the corresponding KubeContext for this platform

        Returns:
            KubeContext with platform details
        """
        return KubeContext(self.kubernetes_context, '', self.namespace)
