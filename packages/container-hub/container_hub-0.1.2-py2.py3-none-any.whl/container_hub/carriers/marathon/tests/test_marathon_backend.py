import pytest
import json
from unittest.mock import MagicMock, patch
from datetime import datetime
from container_hub.carriers.marathon.backend import MarathonBackend
from container_hub.models import (
    LogLevel,
    MountPoint,
    MarathonBackendConfig,
    ContainerConfig,
    EnvVar,
    Label,
    MarathonConstraint,
)


@pytest.fixture
def marathon_backend():
    config = MarathonBackendConfig(
        "http://marathon_url/",
        "my_network",
        constraints=[MarathonConstraint("api", "CLUSTER", "v3")],
    )
    return MarathonBackend(config)


def test_container_hosts(marathon_backend: MarathonBackend):
    with patch("container_hub.carriers.marathon.backend.MarathonClient") as client:
        task = MagicMock()
        task.app_id = "simulation-112"
        task.host = "localhost"
        client().list_tasks.return_value = [task]
        hosts = marathon_backend.container_hosts()
        assert hosts == {"simulation-112": "localhost"}


def test_container_list(marathon_backend: MarathonBackend):
    with patch("container_hub.carriers.marathon.backend.MarathonClient") as client:
        container = MagicMock()
        container.labels = {"simulation_id": "112"}
        client().list_apps.return_value = [container]
        containers = marathon_backend.container_list()
        assert containers == [
            "112",
        ]


def test_container_ips(marathon_backend: MarathonBackend):
    with patch("container_hub.carriers.marathon.backend.MarathonClient") as client:
        task = MagicMock()
        task.app_id = "simulation-112"
        ip_address = MagicMock()
        ip_address.ip_address = "127.0.0.1"
        task.ip_addresses = [ip_address]
        client().list_tasks.return_value = [task]
        ip_addresses = marathon_backend.container_ips()
        assert ip_addresses == {"simulation-112": "127.0.0.1"}


def test_up(marathon_backend: MarathonBackend):
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

    with patch("container_hub.carriers.marathon.backend.MarathonClient") as client:
        app = MagicMock()
        app.id = "simulation-112"
        client().create_app.return_value = app
        app_id = marathon_backend.up(container_config)
        assert app_id == "simulation-112"

        # Check call args
        to_check = {
            "args": [
                "python",
                "service.py",
                "redis1",
                "/model.ini",
                12,
                dt.isoformat(),
                "3600",
                "3600",
                "initialize",
                "0",
                "0",
                "True",
                "gridadmin_url",
                "tables_download_url",
            ],
            "constraints": [["api", "CLUSTER", "v3"]],
            "container": {
                "docker": {
                    "forcePullImage": False,
                    "image": "my_image",
                    "network": "BRIDGE",
                    "parameters": [{"key": "network", "value": "my_network"}],
                    "privileged": False,
                },
                "type": "DOCKER",
                "volumes": [
                    {"containerPath": "/mnt", "hostPath": "/local", "mode": "RW"}
                ],
            },
            "cpus": 2,
            "env": {
                "LOG_LEVEL": "DEBUG",
                "RESULT_PATH": "base_result_path/simulation-12",
                "env": "1",
            },
            "labels": {"name": "value", "simulation_id": "12"},
            "mem": 512,
        }

        assert client().create_app.call_args[0][1].to_json() == json.dumps(to_check)


def test_down(marathon_backend: MarathonBackend):
    with patch("container_hub.carriers.marathon.backend.MarathonClient") as client:
        app = MagicMock()
        app.id = "simulation-112"
        client().list_apps.return_value = [app]
        marathon_backend.down("112")
