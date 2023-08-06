CONTAINER_HUB_CARRIER = "marathon"
CONTAINER_HUB_CLIENT_URL = "http://marathon_url/"
CONTAINER_HUB_NETWORK_NAME = "threedi_backend"
CONTAINER_HUB_IMAGE_NAME = "testimage"
CONTAINER_HUB_CONTAINER_LOG_LEVEL = "DEBUG"
CONTAINER_HUB_MAX_CPU = 2

CONTAINER_HUB_REDIS_HOST = "redis"
CONTAINER_HUB_BASE_MODEL_PATH = "/models"
CONTAINER_HUB_BASE_RESULT_PATH = "/results"

CONTAINER_HUB_MOUNT_POINTS = {
    "local_path_1": {"bind": "mount_path_1", "ro": True},
    "local_path_2": {"bind": "mount_path_2", "ro": False},
}

COMTAINER_HUB_CONSTRAINTS = [
    ["api", "CLUSTER", "v3"],
]
