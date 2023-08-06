CONTAINER_HUB_DEBUG = True
CONTAINER_HUB_CARRIER = "docker"
CONTAINER_HUB_CLIENT_URL = "unix://var/run/docker.sock"
CONTAINER_HUB_NETWORK_NAME = "threedi_backend"  # "threedi_backend"
CONTAINER_HUB_IMAGE_NAME = "testimage"
CONTAINER_HUB_CONTAINER_LOG_LEVEL = "DEBUG"
CONTAINER_HUB_MAX_CPU = 2

# harbor.lizard.net/threedi/threedicore:1.4.15.devtest_3"
CONTAINER_HUB_REDIS_HOST = "redis"  # "redis"
CONTAINER_HUB_BASE_MODEL_PATH = "/models"
# # Location where to write the results of the calccore.
CONTAINER_HUB_BASE_RESULT_PATH = "/results"


CONTAINER_HUB_MOUNT_POINTS = {
    "local_path_1": {"bind": "mount_path_1", "ro": True},
    "local_path_2": {"bind": "mount_path_2", "ro": False},
}
