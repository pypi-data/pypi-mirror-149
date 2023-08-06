import logging
from pathlib import Path
from typing import Dict, List
from typing import Iterator
from typing import Tuple
from container_hub.models import MarathonBackendConfig
from container_hub.models import ContainerConfig
from functools import cached_property
import marathon.exceptions
from marathon import MarathonApp
from marathon.models.app import MarathonTask
from marathon.models.container import MarathonContainer
from marathon.models.container import MarathonContainerVolume
from marathon.models.container import MarathonDockerContainer
from marathon.models.constraint import MarathonConstraint
from marathon import MarathonClient
from container_hub.exceptions import CarrierError

logger = logging.getLogger(__name__)


class MachineManagerException(Exception):
    pass


def _task_generator(client: MarathonClient) -> Iterator[Tuple[MarathonTask, str]]:
    tasks = client.list_tasks()
    for task in tasks:
        app_name = task.app_id.strip("/")
        yield task, app_name


def _del_app(client: MarathonClient, app_name: str) -> bool:
    """
    wrapper around the ``client.delete_app`` call

    :returns True if the app has been deleted, False otherwise
    """
    try:
        client.delete_app(app_name, force=True)
    except marathon.exceptions.NotFoundError:
        # not found; assume that the app is deleted
        logger.exception("Failed to delete app %s.", app_name)
        return False

    logger.info("Deleted app %s.", app_name)
    return True


class MarathonBackend:
    """
    Backend for starting Docker instances via Docker
    """

    def __init__(self, config: MarathonBackendConfig):
        self.config = config

    @cached_property
    def client(self) -> MarathonClient:
        return MarathonClient(self.config.client_url)

    def container_hosts(self) -> Dict[str, str]:
        d = {}
        for task, app_name in _task_generator(self.client):
            d[app_name] = task.host
        return d

    def container_ips(self) -> Dict[str, str]:
        d = {}
        for task, app_name in _task_generator(self.client):
            _ip = task.ip_addresses[0]
            d[app_name] = _ip.ip_address
        return d

    def container_list(self) -> List[str]:
        sim_uids = []
        apps = self.client.list_apps()
        for app in apps:
            # v3 apps all have a simulation id label
            sim_uid = app.labels.get("simulation_id")
            if not sim_uid:
                continue
            sim_uids.append(sim_uid)
        return sim_uids

    def up(self, container_config: ContainerConfig) -> str:
        """Create a MarathonApp instance."""
        name = f"simulation-{container_config.sim_uid}"

        labels = dict([(x.name, x.value) for x in container_config.labels])
        labels.update({"simulation_id": f"{container_config.sim_uid}"})

        docker_container = MarathonDockerContainer(
            image=container_config.image_name,
            network="BRIDGE",
            parameters=[{"key": "network", "value": self.config.network_name}],
        )

        volumes = []  # == mounts

        skip_model_mount: bool = all(
            [
                x
                for x in [
                    container_config.gridadmin_download_url,
                    container_config.tables_download_url,
                ]
            ]
        )

        for mount in container_config.mount_points:
            if skip_model_mount and mount.mount_path == "/models":
                # Skip mounting models
                continue

            volumes.append(
                MarathonContainerVolume(
                    container_path=mount.mount_path,
                    host_path=mount.local_path,
                    mode="RO" if mount.read_only else "RW",
                )
            )

        logger.debug("Volumes %s", volumes)

        # docker container with volumes
        container = MarathonContainer(docker=docker_container, volumes=volumes)
        result_path = container_config.base_result_path / Path(name)

        envs = dict([(f"{x.name}", f"{x.value}") for x in container_config.envs])
        # environment variables for container
        envs.update({"RESULT_PATH": result_path.as_posix()})

        if container_config.container_log_level is not None and "LOG_LEVEL" not in envs:
            envs.update({"LOG_LEVEL": f"{container_config.container_log_level.value}"})

        constraints = []

        if self.config.constraints:
            constraints = [
                MarathonConstraint(
                    constraint.param, constraint.operator, constraint.value
                )
                for constraint in self.config.constraints
            ]

        # all args must be strings
        args = [
            "python",
            "service.py",
            container_config.redis_host,
            container_config.model_config,
            container_config.sim_uid,
            container_config.sim_ref_datetime.isoformat(),
            str(container_config.end_time),
            str(container_config.duration),
            container_config.start_mode,
            str(container_config.pause_timeout),
            str(container_config.max_rate),
            str(container_config.clean_up_files),
        ]

        if container_config.gridadmin_download_url is not None:
            args.append(str(container_config.gridadmin_download_url))
        if container_config.tables_download_url is not None:
            args.append(str(container_config.tables_download_url))

        marathon_app_definition = MarathonApp(
            args=args,
            container=container,
            mem=container_config.session_memory,
            cpus=container_config.max_cpu,
            env=envs,
            labels=labels,
            constraints=constraints,
        )

        try:
            app = self.client.create_app(name, marathon_app_definition)
        except marathon.exceptions.MarathonHttpError as err:
            logger.exception("Failed to create app %s with error %s", name, err)
            raise CarrierError(err)
        logger.info(f"App {app.id} started")
        return app.id

    def down(self, sim_uid: str):
        """Remove the given app."""

        app_name = f"simulation-{sim_uid}"

        # should return a single marathon.models.app.MarathonApp instance
        apps = self.client.list_apps(app_id=app_name)
        if not apps:
            logger.warning(
                "App not found; assuming that the app has already been deleted"
            )
            return

        if len(apps) > 1:
            msg = (
                f"Found more than one app that matches the name {app_name}. "
                f"Trying to delete all of them now..."
            )
            logger.warning(msg)
            for app in apps:
                _del_app(self.client, app.id)
            return

        app = apps[0]
        _del_app(self.client, app.id)
