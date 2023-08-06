from .exceptions import InvalidConfiguration


def get_backend(settings, prefix="CONTAINER_HUB"):
    """
    Get a backend based on simple-settings or Django settings object.

    Uses `CONTAINER_HUB_CARRIER` = ["docker", "marathon"] to determine
    the backend.
    """
    if not hasattr(settings, f"{prefix}_CARRIER"):
        raise InvalidConfiguration(f"{prefix}_CARRIER is a mandatory setting")
    opt = str(getattr(settings, f"{prefix}_CARRIER")).lower()

    if opt == "docker":
        from container_hub.carriers.docker.backend import (
            DockerBackend,
            DockerBackendConfig,
        )

        return DockerBackend(DockerBackendConfig.from_settings(settings, prefix))
    elif opt == "marathon":
        from container_hub.carriers.marathon.backend import (
            MarathonBackend,
            MarathonBackendConfig,
        )

        return MarathonBackend(MarathonBackendConfig.from_settings(settings, prefix))
    elif opt == "kubernetes":
        from container_hub.carriers.kubernetes.backend import (
            KubernetesBackend,
            KubernetesBackendConfig,
        )

        return KubernetesBackend(
            KubernetesBackendConfig.from_settings(settings, prefix)
        )

    raise InvalidConfiguration(
        f"Unknown carrier {opt} option, should either be 'docker' or 'marathon'"
    )
