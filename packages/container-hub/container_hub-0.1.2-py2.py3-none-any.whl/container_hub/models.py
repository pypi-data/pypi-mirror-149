from __future__ import annotations
import dataclasses
from pathlib import Path
from dataclasses import dataclass, field, fields, _MISSING_TYPE
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime
from .exceptions import InvalidConfiguration
from slugify import slugify


class LogLevel(Enum):
    info = "INFO"
    debug = "DEBUG"
    warning = "WARNING"


@dataclass
class MountPoint:
    local_path: str
    mount_path: str
    read_only: bool = True

    @property
    def name(self) -> str:
        return slugify(self.local_path)


def create_klass(cls, settings, prefix: str):
    """
    Create cls from config parameters in settings.

    The fields of cls should be present in upper-case prefixed with the prefix and "_".
    """
    kwargs = {}

    for field in fields(cls):
        attr_name = f"{prefix}_{field.name.upper()}"

        if (
            isinstance(field.default, _MISSING_TYPE)
            and isinstance(field.default_factory, _MISSING_TYPE)
            and not hasattr(settings, attr_name)
        ):
            raise InvalidConfiguration(f"{attr_name} is a mandatory setting")

        if hasattr(settings, attr_name):
            kwargs[field.name] = getattr(settings, attr_name)

    # [['api', 'CLUSTER', 'v3'], ]
    if "constraints" in kwargs and isinstance(kwargs["constraints"], list):
        kwargs["constraints"] = [MarathonConstraint(*x) for x in kwargs["constraints"]]

    return cls(**kwargs)


@dataclass
class DockerBackendConfig:
    client_url: str  # URL to docker or marathon
    network_name: str  # network to use
    debug: bool = False

    @classmethod
    def from_settings(cls, settings, prefix="CONTAINER_HUB") -> "DockerBackendConfig":
        """
        Populate DockerBackendConfig from simple-settings, Django settings
        or similair object.
        """
        return create_klass(cls, settings, prefix)


@dataclass
class MarathonConstraint:
    param: str
    operator: str
    value: str


@dataclass
class MarathonBackendConfig(DockerBackendConfig):
    constraints: List[MarathonConstraint] = field(default_factory=list)

    @classmethod
    def from_settings(cls, settings, prefix="CONTAINER_HUB") -> "MarathonBackendConfig":
        """
        Populate MarathonBackendConfig from simple-settings, Django settings
        or similair object.
        """
        return create_klass(cls, settings, prefix)


@dataclass
class KubernetesBackendConfig:
    client_url: str  # URL to docker or marathon
    # Kubernetes namespace to deploy to
    namespace: str = "default"

    @classmethod
    def from_settings(
        cls, settings, prefix="CONTAINER_HUB"
    ) -> "KubernetesBackendConfig":
        """
        Populate KubernetesBackendConfig from simple-settings, Django settings
        or similair object.
        """
        return create_klass(cls, settings, prefix)


@dataclass
class EnvVar:
    name: str
    value: str


@dataclass
class Label:
    name: str
    value: str


@dataclass
class ContainerConfig:
    image_name: str  # threedicore image name
    base_result_path: Path  # path for results
    sim_uid: str
    sim_ref_datetime: datetime
    end_time: int
    duration: int
    pause_timeout: int
    start_mode: str
    model_config: str
    max_cpu: int  # max CPU's to use
    session_memory: int  # max memory
    envs: List[EnvVar]
    labels: List[Label]
    max_rate: float = 0.0
    clean_up_files: bool = False
    gridadmin_download_url: Optional[str] = None
    tables_download_url: Optional[str] = None
    mount_points: List[MountPoint] = field(default_factory=list)
    redis_host: str = "redis"  # Local redis host
    container_log_level: LogLevel = LogLevel.info


# Kubernetes dataclasses.
# These are much more generic than the Docker/Marathon ContainerConfig


@dataclass
class KubernetesContainer:
    name: str
    image: str  # Docker image
    args: List[str]  # command start up args
    envs: List[EnvVar] = field(default_factory=list)
    labels: List[Label] = field(default_factory=list)
    mount_points: List[MountPoint] = field(default_factory=list)
    ports: List[int] = field(default_factory=list)

    @classmethod
    def from_dict(cls, values: Dict) -> "KubernetesContainer":
        return KubernetesContainer(
            name=values.get("name"),
            image=values.get("image"),
            args=values.get("args"),
            envs=[EnvVar(key, value) for key, value in values.get("envs", {}).items()],
            labels=[
                Label(key, value) for key, value in values.get("labels", {}).items()
            ],
            mount_points=[
                MountPoint(key, value["bind"], value["ro"])
                for key, value in values.get("mounts", {}).items()
            ],
            ports=values.get("ports", []),
        )


@dataclass
class KubernetesJobConfig:
    name: str
    redis_config: KubernetesContainer
    scheduler_config: KubernetesContainer
    scheduler_worker_config: KubernetesContainer
    simulation_config: KubernetesContainer
    annotations: List[Label] = field(default_factory=list)
    labels: List[Label] = field(default_factory=list)

    @property
    def mount_points(self) -> List[MountPoint]:
        """
        Combined list of mount_points
        """
        mount_points = []
        for mount_point in (
            self.redis_config.mount_points
            + self.scheduler_config.mount_points
            + self.scheduler_worker_config.mount_points
            + self.simulation_config.mount_points
        ):
            if mount_point not in mount_points:
                mount_points.append(mount_point)
        return mount_points

    @classmethod
    def from_settings(
        cls, name: str, settings, prefix="CONTAINER_HUB"
    ) -> "KubernetesJobConfig":
        """
        Load KubernetesJobConfig from supplied values in `CONTAINER_HUB_KUBERNETES_CONTAINER_DEFAULTS`
        """
        cfg = getattr(settings, f"{prefix}_KUBERNETES_CONTAINER_DEFAULTS")

        return KubernetesJobConfig(
            name=name,
            redis_config=KubernetesContainer.from_dict(cfg["REDIS"]),
            scheduler_config=KubernetesContainer.from_dict(cfg["SCHEDULER"]),
            scheduler_worker_config=KubernetesContainer.from_dict(
                cfg["SCHEDULER_WORKER"]
            ),
            simulation_config=KubernetesContainer.from_dict(cfg["SIMULATION"]),
        )
