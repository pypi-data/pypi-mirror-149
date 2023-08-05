""" mcli util Entrypoint """
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, cast

from kubernetes import client
from kubernetes import config as k8s_config
from kubernetes.client.api_client import ApiClient

from mcli import config
from mcli.models.mcli_platform import MCLIPlatform
from mcli.serverside.platforms.registry import PlatformRegistry
from mcli.utils.utils_kube_labels import label

IGNORE_NAMESPACES = [
    'default', 'fleet-system', 'ingress-nginx', 'security-scan', 'nick', 'nodekiller', 'jenkins', 'jenkinsnext',
    'mining', 'avery-daemons'
]


def valid_namespace(namespace: str) -> bool:
    if namespace in IGNORE_NAMESPACES:
        return False
    for start in ('cattle-', 'kube-', 'it-'):
        if namespace.startswith(start):
            return False
    return True


class NodeStatus(Enum):
    UNAVAILABLE = 'unavailable'
    READY = 'ready'


@dataclass
class NodeInfo():
    name: str
    gpu_available: int
    gpu_used: int
    cpu_available: int
    cpu_used: int
    instance_size: str
    status: NodeStatus


@dataclass
class JobInfo():
    name: str
    instance_size: str
    node_name: str
    namespace: str
    gpu_used: int
    cpu_used: int
    age: str
    priority: str


def _convert_cpus(cpu):
    if isinstance(cpu, str) and cpu.endswith('m'):
        return cpu[:-1]
    return cpu


def get_nodes(cl: client.CoreV1Api, api: ApiClient) -> List[NodeInfo]:
    nodes = cl.list_node()

    node_list: List[NodeInfo] = []
    for node in nodes.items:
        node_data: Dict[str, Any] = cast(Dict[str, Any], api.sanitize_for_serialization(node))
        metadata = node_data.get('metadata', {})
        labels = metadata.get('labels', {})
        instance_size = labels.get(label.mosaic.cloud.INSTANCE_SIZE, None)
        instance_size_legacy = labels.get(label.mosaic.NODE_CLASS, '-')
        allocatable = node_data.get('status', {}).get('allocatable', {})
        available = node_data.get('spec', {}).get('unschedulable', None) is None
        name = metadata.get('name', '-')
        data = {
            'name': name,
            'gpu_available': int(allocatable.get(label.nvidia.GPU, 0)),
            'gpu_used': 0,
            'cpu_available': int(_convert_cpus(allocatable.get('cpu', 0))),
            'cpu_used': 0,
            'instance_size': instance_size or instance_size_legacy,
            'status': NodeStatus.READY if available else NodeStatus.UNAVAILABLE,
        }
        node_list.append(NodeInfo(**data))
    return node_list


def get_jobs_from_namespace(
    cl: client.CoreV1Api,
    api: ApiClient,
    namespace: str,
    platform: MCLIPlatform,
) -> List[JobInfo]:

    jobs: List[JobInfo] = []
    try:
        pods = cl.list_namespaced_pod(namespace=namespace,
                                      field_selector='status.phase!=Succeeded,status.phase!=Failed')
    except Exception as _:  # pylint: disable=broad-except

        return jobs
    for pod in pods.items:
        pod_data: Dict[str, Any] = cast(Dict[str, Any], api.sanitize_for_serialization(pod))
        metadata = pod_data.get('metadata', {})
        pod_name = metadata.get('name', 'noname')
        # Assuming one container per pod
        spec = pod_data.get('spec', {})
        node_name = spec.get('nodeName', 'Unassigned')
        containers = spec.get('containers', [])
        if len(containers) == 0:
            continue
        container = containers[0]
        resources = container.get('resources', {}).get('limits', '')

        status = pod_data.get('status', {})
        start_time = status.get('startTime', None)
        if start_time is None:
            start_time = metadata.get('creationTimestamp')
        start_time = str(start_time)
        age = _print_timedelta(datetime.now(timezone.utc) - datetime.fromisoformat(start_time))
        priority_class_name = spec.get('priorityClassName', None)
        priority_class = 'unknown'
        if priority_class_name:
            # TODO: Abstract and remove
            k8s_platform = PlatformRegistry().get_k8s_platform(platform=platform)
            reverse_priority = {v: k for k, v in k8s_platform.priority_class_labels.items()}
            priority_class = reverse_priority.get(priority_class_name, 'unknown')

        labels = metadata.get('labels', {})
        instance_size = labels.get(label.mosaic.cloud.INSTANCE_SIZE, None)
        instance_size_legacy = labels.get(label.mosaic.NODE_CLASS, '-')
        data = {
            'name': pod_name,
            'instance_size': instance_size or instance_size_legacy,
            'node_name': node_name,
            'namespace': namespace,
            'gpu_used': int(resources.get(label.nvidia.GPU)),
            'cpu_used': int(_convert_cpus(resources.get('cpu'))),
            'age': age,
            'priority': priority_class,
        }
        jobs.append(JobInfo(**data))

    return jobs


def get_util(platform: str, **kwargs) -> int:
    del kwargs

    conf = config.MCLIConfig.load_config()
    platforms = []
    if platform == 'all':
        platforms = conf.platforms
    else:
        platforms += [x for x in conf.platforms if platform == x.name]

    print(platforms)
    for plat in platforms:
        api = k8s_config.new_client_from_config(context=plat.kubernetes_context)
        cl = client.CoreV1Api(api_client=api)
        node_list = get_nodes(cl=cl, api=api)
        del node_list

        namespaces = [str(n.metadata.name) for n in cl.list_namespace().items]
        namespaces = [x for x in namespaces if valid_namespace(x)]
        for namespace in namespaces:
            jobs = get_jobs_from_namespace(cl, api, namespace, plat)
            for job in jobs:
                print(job)

        print(namespaces)

    return 0


def _print_timedelta(delta: timedelta):
    # strftime cannot be used with timedelta

    seconds = delta.total_seconds()
    if seconds < 60:
        return f'{int(seconds)}s'
    elif seconds < 3600:
        return f'{int(seconds/60)}min'
    elif seconds < 24 * 3600:
        return f'{int(seconds/3600)}hr'
    else:
        return f'{int(seconds/3600/24)}d'
