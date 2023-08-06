import pytest
from dataclasses import asdict
from container_hub import get_backend
from container_hub.carriers.docker.backend import DockerBackend
from container_hub.carriers.marathon.backend import MarathonBackend
from container_hub.carriers.kubernetes.backend import KubernetesBackend
from container_hub.models import KubernetesJobConfig
from simple_settings import LazySettings


@pytest.fixture
def docker_simple_settings():
    # os.environ.update({"SIMPLE_SETTINGS": "tests.test_files.docker_settings"})
    yield LazySettings("tests.test_files.docker_settings")


@pytest.fixture
def marathon_simple_settings():
    yield LazySettings("tests.test_files.marathon_settings")


@pytest.fixture
def kubernetes_simple_settings():
    yield LazySettings("tests.test_files.kubernetes_settings")


def test_loading_docker_backend(docker_simple_settings):
    backend = get_backend(docker_simple_settings)
    assert isinstance(backend, DockerBackend)


def test_loading_marathon_backend(marathon_simple_settings):
    backend = get_backend(marathon_simple_settings)
    assert isinstance(backend, MarathonBackend)


def test_loading_kubernetes_backend(kubernetes_simple_settings):
    backend = get_backend(kubernetes_simple_settings)
    assert backend.config.namespace == "threedi"
    assert isinstance(backend, KubernetesBackend)


# Test loading kubernetes container defaults
def test_loading_kubernetes_defaults(kubernetes_simple_settings):
    config = KubernetesJobConfig.from_settings("sim4234", kubernetes_simple_settings)
    assert asdict(config) == {
        "name": "sim4234",
        "redis_config": {
            "name": "redis",
            "image": "redis:5.0.3-alpine",
            "args": ["sh", "-c", "rm -rf /data/dump.rdb && redis-server --save "],
            "envs": [],
            "labels": [],
            "mount_points": [],
            "ports": [6379],
        },
        "scheduler_config": {
            "name": "scheduler",
            "image": "harbor.lizard.net/threedi/scheduler:latest",
            "args": ["python3", "/code/scheduler.py", "localhost"],
            "envs": [
                {
                    "name": "DJANGO_SETTINGS_MODULE",
                    "value": "threedi_scheduler.developmentsettings",
                },
                {"name": "REDIS_HOST", "value": "localhost"},
            ],
            "labels": [],
            "mount_points": [
                {
                    "local_path": "/local/path/one",
                    "mount_path": "mount_path_1",
                    "read_only": True,
                },
                {
                    "local_path": "/local/path/two",
                    "mount_path": "mount_path_2",
                    "read_only": False,
                },
            ],
            "ports": [],
        },
        "scheduler_worker_config": {
            "name": "scheduler_worker",
            "image": "harbor.lizard.net/threedi/scheduler:latest",
            "args": [
                "python3",
                "/code/manage.py",
                "wait_for_redis_runworker",
                "condition_worker",
                "event_worker",
            ],
            "envs": [
                {
                    "name": "DJANGO_SETTINGS_MODULE",
                    "value": "threedi_scheduler.developmentsettings",
                },
                {"name": "REDIS_HOST", "value": "localhost"},
            ],
            "labels": [],
            "mount_points": [
                {
                    "local_path": "/local/path/one",
                    "mount_path": "mount_path_1",
                    "read_only": True,
                },
                {
                    "local_path": "/local/path/two",
                    "mount_path": "mount_path_2",
                    "read_only": False,
                },
            ],
            "ports": [],
        },
        "simulation_config": {
            "name": "simulation",
            "image": "harbor.lizard.net/threedi/threedicore:2.16.1-2.2.5",
            "args": ["python", "service.py", "localhost"],
            "envs": [{"name": "RESULTS_PATH", "value": "/results"}],
            "labels": [],
            "mount_points": [
                {
                    "local_path": "/local/path/one",
                    "mount_path": "mount_path_1",
                    "read_only": True,
                },
                {
                    "local_path": "/local/path/two",
                    "mount_path": "mount_path_2",
                    "read_only": False,
                },
            ],
            "ports": [],
        },
        "annotations": [],
        "labels": [],
    }
