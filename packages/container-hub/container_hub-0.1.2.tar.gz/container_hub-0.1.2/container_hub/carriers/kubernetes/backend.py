from typing import Dict, List
from kubernetes import config as client_config
from kubernetes.client import Configuration, ApiClient, BatchV1Api, CoreV1Api
from container_hub.exceptions import CarrierError
from kubernetes.client.models import V1JobList
from container_hub.models import (
    KubernetesBackendConfig,
    KubernetesJobConfig,
    KubernetesContainer,
)
from functools import cached_property


from hikaru.model.rel_1_20 import (
    Job,
    JobSpec,
    ObjectMeta,
    LabelSelector,
    PodTemplateSpec,
    PodSpec,
    Container,
    ResourceRequirements,
    ContainerPort,
    EnvVar,
    VolumeMount,
    Volume,
    HostPathVolumeSource,
)


# Accessing host (laptop) from within k8s cluster
K3S_HOST_DNS_NAME = "host.k3d.internal"
MINIKUBE_HOST_DNS_NAME = "host.minikube.internal"


class KubernetesBackend:
    """
    Backend for starting Docker instances via Docker
    """

    def __init__(self, config: KubernetesBackendConfig, in_cluster=True):
        self.config = config
        self.in_cluster = in_cluster


    @cached_property
    def configuration(self) -> Configuration:
        configuration = Configuration(host=self.config.client_url)
        if self.in_cluster:
            client_config.load_incluster_config(configuration)

        return configuration

    def container_hosts(self) -> Dict[str, str]:
        return {}

    def pod_ip(self, job_name: str) -> str:
        """
        Get a specific pod ip, based on job_name (simulation-xxx)
        """
        with ApiClient(self.configuration) as api_client:
            api = CoreV1Api(api_client)
            results = api.list_namespaced_pod(
                namespace="default", label_selector=f"job-name={job_name}")
            if len(results.items) != 1:
                raise CarrierError(f"Incorrect number of pods returned: {results}")
            return results.items[0].status.pod_ip

    def container_ips(self) -> Dict[str, str]:
        return {}

    def container_list(self) -> List[str]:
        with ApiClient(self.configuration) as api_client:
            api = BatchV1Api(api_client)
            # TODO: check pagination
            job_list: V1JobList = api.list_namespaced_job(
                namespace=self.config.namespace
            )
            return [job.metadata.name for job in job_list.items]

    def up(self, job_config: KubernetesJobConfig) -> str:
        """
        Create Kubernetes job for simulation
        """
        job = get_simulation_job(job_config)
        with ApiClient(self.configuration) as api_client:
            job = job.create(namespace=self.config.namespace, client=api_client)
        return job_config.name

    def down(self, sim_uid: str):
        """Remove the given app."""
        name = f"simulation-{sim_uid}"
        with ApiClient(self.configuration) as api_client:
            api = BatchV1Api(api_client)
            api.delete_namespaced_job(namespace=self.config.namespace, name=name)


def get_simulation_job(cfg: KubernetesJobConfig) -> Job:
    return Job(
        apiVersion="apps/v1",
        kind="Job",
        metadata=ObjectMeta(
            name=cfg.name,
            annotations={x.name: x.value for x in cfg.annotations},
            labels={x.name: x.value for x in cfg.labels},
        ),
        spec=JobSpec(
            selector=LabelSelector(matchLabels={"app": "simulation"}),
            template=PodTemplateSpec(
                metadata=ObjectMeta(
                    annotations={x.name: x.value for x in cfg.annotations},
                    labels={"app": "simulation"},
                ),
                spec=PodSpec(
                    containers=[
                        get_container(cfg.redis_config),
                        get_container(cfg.scheduler_config),
                        get_container(cfg.scheduler_worker_config),
                        get_container(cfg.simulation_config),
                    ],
                    volumes=[
                        Volume(
                            name=mount.name,
                            hostPath=HostPathVolumeSource(
                                path=mount.local_path, type="Directory"
                            ),
                        )
                        for mount in cfg.mount_points
                    ],
                ),
            ),
        ),
    )

def get_container(cfg: KubernetesContainer) -> Container:
    """
    Get k8s container API resource
    """
    # Might ne needed for local dev:
    #   hostAliases=[HostAlias(f"{HOST_IP}", ["minio"])],

    return Container(
        name=cfg.name,
        image=cfg.image,
        imagePullPolicy="IfNotPresent",
        resources=ResourceRequirements(),
        args=cfg.args,
        env=[
            EnvVar(
                name=envvar.name,
                value=envvar.value,
            )
            for envvar in cfg.envs
        ],
        volumeMounts=[
            VolumeMount(mountPath=mount.mount_path, name=mount.name)
            for mount in cfg.mount_points
        ],
        ports=[ContainerPort(containerPort=port) for port in cfg.ports],
    )
