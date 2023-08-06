CONTAINER_HUB_CARRIER = "kubernetes"
CONTAINER_HUB_CLIENT_URL = "http://kubernetes_url/"
CONTAINER_HUB_NAMESPACE = "threedi"


# Note: Below are defaults that can always be overriden in code before
# sending it to Kubernetes
CONTAINER_HUB_KUBERNETES_CONTAINER_DEFAULTS = {
    "REDIS": {
        "name": "redis",
        "image": "redis:5.0.3-alpine",
        "args": ["sh", "-c", "rm -rf /data/dump.rdb && redis-server --save " ""],
        "ports": [
            6379,
        ],
    },
    "SCHEDULER": {
        "name": "scheduler",
        "image": "harbor.lizard.net/threedi/scheduler:latest",
        "args": ["python3", "/code/scheduler.py", "localhost"],
        "envs": {
            "DJANGO_SETTINGS_MODULE": "threedi_scheduler.developmentsettings",
            "REDIS_HOST": "localhost",
        },
        "mounts": {
            "/local/path/one": {"bind": "mount_path_1", "ro": True},
            "/local/path/two": {"bind": "mount_path_2", "ro": False},
        },
    },
    "SCHEDULER_WORKER": {
        "name": "scheduler_worker",
        "image": "harbor.lizard.net/threedi/scheduler:latest",
        "args": [
            "python3",
            "/code/manage.py",
            "wait_for_redis_runworker",
            "condition_worker",
            "event_worker",
        ],
        "envs": {
            "DJANGO_SETTINGS_MODULE": "threedi_scheduler.developmentsettings",
            "REDIS_HOST": "localhost",
        },
        "mounts": {
            "/local/path/one": {"bind": "mount_path_1", "ro": True},
            "/local/path/two": {"bind": "mount_path_2", "ro": False},
        },
    },
    "SIMULATION": {
        "name": "simulation",
        "image": "harbor.lizard.net/threedi/threedicore:2.16.1-2.2.5",
        "args": ["python", "service.py", "localhost"],
        "envs": {"RESULTS_PATH": "/results"},
        "mounts": {
            "/local/path/one": {"bind": "mount_path_1", "ro": True},
            "/local/path/two": {"bind": "mount_path_2", "ro": False},
        },
    },
}
