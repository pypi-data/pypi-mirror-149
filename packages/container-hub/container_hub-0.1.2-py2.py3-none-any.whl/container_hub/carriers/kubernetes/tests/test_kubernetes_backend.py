import pytest
from unittest.mock import MagicMock, patch
from container_hub.carriers.kubernetes.backend import KubernetesBackend
from simple_settings import LazySettings
from container_hub.models import (
    KubernetesBackendConfig,
    KubernetesJobConfig,
)


@pytest.fixture
def kubernetes_backend():
    config = KubernetesBackendConfig(
        "http://kubernetes/",
        "threedi",
    )
    return KubernetesBackend(config, in_cluster=False)


@pytest.fixture
def kubernetes_simple_settings():
    yield LazySettings("tests.test_files.kubernetes_settings")


def test_container_list(kubernetes_backend: KubernetesBackend):
    with patch("container_hub.carriers.kubernetes.backend.ApiClient") as client:
        job = MagicMock()
        job.metadata.name = "simulation-112"
        job_list = MagicMock()
        job_list.items = [job]
        client().__enter__().call_api.return_value = job_list
        hosts = kubernetes_backend.container_list()
        assert hosts == ["simulation-112"]


def test_pod_ip(kubernetes_backend: KubernetesBackend):
    with patch("container_hub.carriers.kubernetes.backend.ApiClient") as client:
        pod = MagicMock()
        pod.status.pod_ip = "127.0.0.1"
        pod_list = MagicMock()
        pod_list.items = [pod]
        client().__enter__().call_api.return_value = pod_list
        pod_ip = kubernetes_backend.pod_ip("simulation-1")
        assert pod_ip == "127.0.0.1"


def test_up(kubernetes_backend: KubernetesBackend, kubernetes_simple_settings):
    job_config = KubernetesJobConfig.from_settings(
        "simulation-1", kubernetes_simple_settings
    )

    with patch("container_hub.carriers.kubernetes.backend.ApiClient") as client:

        def call_api(*args, body=None, **kwargs):
            return (body, 200, {})

        client().__enter__().call_api = call_api
        name = kubernetes_backend.up(job_config)
        assert name == "simulation-1"


def test_down(kubernetes_backend: KubernetesBackend):
    with patch("container_hub.carriers.kubernetes.backend.ApiClient") as client:
        kubernetes_backend.down("simulation-1")
        client().__enter__().call_api.assert_called()
