import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from container_hub.carriers.docker.backend import DockerBackend
from container_hub.models import (
    LogLevel,
    MountPoint,
    DockerBackendConfig,
    ContainerConfig,
    EnvVar,
    Label,
)
from docker.types import Mount


@pytest.fixture
def docker_backend():
    config = DockerBackendConfig(
        "client_url",
        "my_network",
    )
    return DockerBackend(config)


def test_container_list(docker_backend: DockerBackend):
    with patch("container_hub.carriers.docker.backend.DockerClient") as client:
        container = MagicMock()
        container.name = "simulation-112"
        client().containers.list.return_value = [container]
        containers = docker_backend.container_list()
        assert containers == [
            "112",
        ]


def test_container_ips(docker_backend: DockerBackend):
    with patch("container_hub.carriers.docker.backend.DockerClient") as client:
        container = MagicMock()
        container.name = "simulation-112"
        container.attrs = {
            "NetworkSettings": {
                "Networks": {
                    docker_backend.config.network_name: {"IPAddress": "127.0.0.1"}
                }
            }
        }
        client().containers.list.return_value = [container]
        ip_addresses = docker_backend.container_ips()
        assert ip_addresses == {"simulation-112": "127.0.0.1"}


def test_up(docker_backend: DockerBackend):
    dt = datetime.now()
    container_config = ContainerConfig(
        "my_image",
        "base_result_path",
        12,
        dt,
        3600,
        3600,
        0,
        "initialize",
        "/model.ini",
        2,
        512,
        [EnvVar("env", "1")],
        [Label("name", "value")],
        0,
        True,
        "gridadmin_url",
        "tables_download_url",
        [MountPoint("/local", "/mnt", False)],
        "redis1",
        LogLevel.debug,
    )
    with patch("container_hub.carriers.docker.backend.DockerClient") as client:
        container = MagicMock()
        container.id = 10
        client().containers.run.return_value = container
        container_id = docker_backend.up(container_config)
        assert container_id == 10

        # Check all params for DockerClient().containers.run
        to_check = {
            "image": "my_image",
            "command": f"python service.py redis1 /model.ini 12 {dt.isoformat()} 3600 3600 initialize 0 0 True gridadmin_url tables_download_url",
            "name": "simulation-12",
            "network": "my_network",
            "mounts": [
                Mount(
                    **{
                        "target": "/mnt",
                        "source": "/local",
                        "type": "bind",
                        "read_only": False,
                    }
                )
            ],
            "environment": {
                "env": "1",
                "RESULT_PATH": "base_result_path/simulation-12",
                "LOG_LEVEL": "DEBUG",
            },
            "detach": True,
            "labels": {"name": "value", "simulation_id": "12"},
        }
        assert client().containers.run.call_args[1] == to_check


def test_down(docker_backend: DockerBackend):
    with patch("container_hub.carriers.docker.backend.DockerClient") as client:
        container = MagicMock()
        container.id = 112
        client().containers.get.return_value = container
        container_id = docker_backend.down("112")
        assert container_id == 112
