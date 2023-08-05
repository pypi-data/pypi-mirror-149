""" MCLI Mounted Secret """
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Set, Type

from kubernetes import client

from mcli.models import MCLIGenericSecret, SecretType
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob, MCLIVolume


@dataclass
class MCLIMountedSecret(MCLIGenericSecret):
    """Secret class for generic secrets that will be mounted to run pods as files
    """
    mount_path: Optional[str] = None

    @property
    def required_packing_fields(self) -> Set[str]:
        return set(self.disk_skipped_fields + ['mount_path'])

    @classmethod
    def from_generic_secret(
        cls: Type[MCLIMountedSecret],
        generic_secret: MCLIGenericSecret,
        mount_path: str,
    ) -> MCLIMountedSecret:
        return cls(
            name=generic_secret.name,
            value=generic_secret.value,
            secret_type=SecretType.mounted,
            mount_path=mount_path,
        )

    def add_to_job(self, kubernetes_job: MCLIK8sJob, permissions: int = 420) -> bool:
        assert self.mount_path is not None
        path = Path(self.mount_path)
        secret_volume = client.V1Volume(
            name=self.name,
            secret=client.V1SecretVolumeSource(
                secret_name=self.name,
                items=[client.V1KeyToPath(key='value', path=path.name)],
                default_mode=permissions,
            ),
        )
        secret_mount = client.V1VolumeMount(
            name=self.name,
            mount_path=str(path.parent),
            read_only=True,
        )
        mcli_volume = MCLIVolume(volume=secret_volume, volume_mount=secret_mount)
        kubernetes_job.add_volume(volume=mcli_volume)
        return True
