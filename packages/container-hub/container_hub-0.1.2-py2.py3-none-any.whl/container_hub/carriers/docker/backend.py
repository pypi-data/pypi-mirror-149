import logging
from container_hub.models import DockerBackendConfig, ContainerConfig
from docker import DockerClient
from docker.types import Mount
from docker.errors import DockerException
from docker.errors import APIError
from docker.errors import ContainerError
from docker.errors import NotFound
from functools import cached_property
from typing import List, Dict
from pathlib import Path

from container_hub.exceptions import CarrierError

logger = logging.getLogger(__name__)


class DockerBackend:
    """
    Backend for starting Docker instances via Docker
    """

    def __init__(self, config: DockerBackendConfig):
        self.config = config

    @cached_property
    def client(self):
        return DockerClient(base_url=self.config.client_url)

    def container_hosts(self) -> Dict[str, str]:
        """
        Always localhost, so return emtpy dict
        """
        return {}

    def container_list(self) -> List[str]:
        """
        Returns a list of simulation_ids
        """
        lc = self.client.containers.list(filters={"label": "simulation_id"})
        return [x.name.lstrip("simulation-") for x in lc]

    def container_ips(self) -> Dict[str, str]:
        """
        Return list of ip addresses
        """
        d = {}
        containers = self.client.containers.list(filters={"label": "simulation_id"})
        for container in containers:
            try:
                ip_address = container.attrs["NetworkSettings"]["Networks"][
                    self.config.network_name
                ]["IPAddress"]
            except KeyError:
                continue
            d[container.name] = ip_address
        return d

    def up(self, container_config: ContainerConfig) -> str:

        """
        Create container based on simulation and threedimodel.

        :returns the container id
        """
        name = f"simulation-{container_config.sim_uid}"
        result_path = container_config.base_result_path / Path(name)
        labels = dict([(x.name, x.value) for x in container_config.labels])
        labels.update({"simulation_id": f"{container_config.sim_uid}"})

        _envs = dict([(f"{x.name}", f"{x.value}") for x in container_config.envs])
        _envs.update({"RESULT_PATH": f"{result_path.as_posix()}"})

        if (
            container_config.container_log_level is not None
            and "LOG_LEVEL" not in _envs
        ):
            _envs.update(
                {f"LOG_LEVEL": f"{container_config.container_log_level.value}"}
            )

        cmd = (
            f"python service.py {container_config.redis_host} {container_config.model_config} "
            f"{container_config.sim_uid} {container_config.sim_ref_datetime.isoformat()} "
            f"{container_config.end_time} {container_config.duration} {container_config.start_mode} "
            f"{container_config.pause_timeout} {container_config.max_rate} {container_config.clean_up_files}"
        )

        skip_model_mount: bool = all(
            [
                x
                for x in [
                    container_config.gridadmin_download_url,
                    container_config.tables_download_url,
                ]
            ]
        )

        if container_config.gridadmin_download_url is not None:
            cmd += f" {container_config.gridadmin_download_url}"
        if container_config.tables_download_url is not None:
            cmd += f" {container_config.tables_download_url}"

        logger.debug("cmd %s", cmd)
        logger.debug("Envs %s", _envs)

        mounts: List[Mount] = []
        for mount in container_config.mount_points:
            if skip_model_mount and mount.mount_path == "/models":
                # Skip mounting models
                continue
            mounts.append(
                Mount(
                    mount.mount_path,
                    mount.local_path,
                    type="bind",
                    read_only=mount.read_only,
                )
            )

        try:
            container = self.client.containers.run(
                image=container_config.image_name,
                command=cmd,
                name=name,
                network=self.config.network_name,
                mounts=mounts,
                environment=_envs,
                detach=True,
                labels=labels,
            )
        except (DockerException, APIError, ContainerError) as err:
            logger.error(err)
            raise CarrierError(err)

        # double check everything went right
        try:
            self.client.containers.get(container.id)
        except (APIError, NotFound) as err:
            logger.error(
                f"simulation container exited prematurely. Could not retrieve "
                f"the container if though it should be running {err}"
            )
            raise CarrierError(err)

        logger.info(f"Started simulation container {container.name}")
        return container.id

    def down(self, sim_uid: str):
        try:
            container = self.client.containers.get(f"simulation-{sim_uid}")
            container_id = container.id
        except (APIError, NotFound) as err:
            logger.error(
                f"Could not get the simulation container, error message: {err}"
            )
            raise CarrierError(err)
        try:
            if not self.config.debug:
                container.remove(force=True)
            else:
                container.kill()
        except APIError as err:
            logger.error(
                f"Could not kill/remove the "
                f"simulation container, error message: {err}"
            )
            raise CarrierError(err)
        logger.info(f"Removed container for simulation {sim_uid}")
        return container_id
