"""Utils for automating K8s contexts"""
from __future__ import annotations

import base64
import copy
import logging
import math
import shlex
import subprocess
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Generator, List, NamedTuple, Optional, Union, cast

from kubernetes import client, config, watch
from urllib3.exceptions import ProtocolError

logger = logging.getLogger(__name__)


def get_client():
    config.load_kube_config()
    return client


def get_context():
    output = subprocess.getoutput('kubectl config current-context')
    return output


def kube_object_to_dict(obj: Any) -> Dict[str, Any]:
    """Convert an object returned by the Kubernetes API to a dict

    Args:
        obj (Kubernetes object): A Kubernetes object returned from the ``kubernetes.client``

    Returns:
        Dict[str, Any]: The serialized dictionary form of the ``obj``
    """
    api_client = client.ApiClient()
    return api_client.sanitize_for_serialization(obj)


class KubeContext():

    def __init__(self, cluster: str, user: str, namespace: Optional[str] = None, **kwargs):
        del kwargs  # unused
        self.cluster = cluster
        self.user = user
        self.namespace = namespace

    def __str__(self) -> str:
        return (f'cluster: {self.cluster},'
                f' \tuser: {self.user}, '
                f" \t{'namespace: ' + self.namespace if self.namespace else ''}")


class StopWatching(Exception):
    """Raised to stop watching a kubernetes watch stream
    """
    pass


class PodEvent(NamedTuple):
    """Pod event status and message
    """
    status: str
    message: str

    def __str__(self) -> str:
        return f'{self.status}: {self.message}'


def watch_pod_events(namespace: str,
                     callback: Callable[[PodEvent], None],
                     name: Optional[str] = None,
                     timeout: Optional[int] = None) -> Optional[PodEvent]:
    """Watch for pod events and call a callback function on each one

    Args:
        namespace: Namespace in which the pod(s) to watch exist.
        callback: Function that takes a PodEvent object and does something with it
        name: Optional pod name to filter by. Defaults to None.
        timeout: Optional timeout for watching pod events. Defaults to None.

    Returns:
        The final PodEvent seen, if one exists
    """
    api = client.CoreV1Api()
    watcher = watch.Watch()
    start = time.time()
    watch_timeout = None
    last_event = None
    field_selector = 'involvedObject.kind=Pod'
    if name:
        field_selector += f',involvedObject.name={name}'
    while True:
        try:
            if timeout is not None:
                watch_timeout = int(math.ceil(timeout - (time.time() - start)))
                if watch_timeout <= 0:
                    break
            for event in watcher.stream(api.list_namespaced_event,
                                        namespace=namespace,
                                        field_selector=field_selector,
                                        timeout_seconds=watch_timeout):
                last_event = PodEvent(event['object'].reason, event['object'].message)
                callback(last_event)

        except ProtocolError:
            pass
        except StopWatching:
            watcher.stop()
            break
    return last_event


def wait_for_job_pods(name: str, namespace: str, timeout: Optional[int] = 30) -> List[str]:
    """Wait for a job's pods to spawn and retun a list of pod names

    Note: This function currently only works with single-pod jobs. As such, the list of
    pod names will always be of length 1 if a pod spawns within the timeout.

    Args:
        name: Name of the job
        namespace: Namespace in which the job exists
        timeout: Optional timeout for how long to wait for pod(s) to spawn. `None` can be
            passed to disable the timeout. Default 30.

    Returns:
        List of pod names
    """

    api = client.CoreV1Api()
    watcher = watch.Watch()
    start = time.time()
    watch_timeout = None
    field_selector = f'involvedObject.kind=Job,involvedObject.name={name}'
    pod_names = []
    while True:
        try:
            if timeout is not None:
                watch_timeout = int(math.ceil(timeout - (time.time() - start)))
                if watch_timeout <= 0:
                    break
            for event in watcher.stream(api.list_namespaced_event,
                                        namespace=namespace,
                                        field_selector=field_selector,
                                        timeout_seconds=watch_timeout):

                if event['object'].reason == 'SuccessfulCreate':
                    pod_name = event['object'].message.replace('Created pod: ', '').strip()
                    pod_names.append(pod_name)
                    raise StopWatching

        except ProtocolError:
            pass
        except StopWatching:
            watcher.stop()
            break
    return pod_names


def wait_for_pod_start(name: str, namespace: str, timeout: Optional[int] = 30) -> bool:
    """Wait for the specified pod to start

    Args:
        name: Name of the pod
        namespace: Namespace in which the pod exists
        timeout: Optional timeout for how long to wait for pod to start. `None` can be
            passed to disable the timeout. Default 30.

    Returns:
        True if pod started, otherwise False
    """
    api = client.CoreV1Api()
    watcher = watch.Watch()
    start = time.time()
    watch_timeout = None
    started = False
    while True:
        try:
            if timeout is not None:
                watch_timeout = int(math.ceil(timeout - (time.time() - start)))
                if watch_timeout <= 0:
                    break
            for event in watcher.stream(api.list_namespaced_pod,
                                        namespace=namespace,
                                        timeout_seconds=watch_timeout,
                                        field_selector=f'metadata.name={name}'):
                pod_obj = event['object']
                if pod_obj.status.phase == 'Running':
                    started = True
                    raise StopWatching

        except ProtocolError:
            pass
        except StopWatching:
            watcher.stop()
            break
    return started


def connect_to_pod(name: str, context: KubeContext) -> bool:
    """Connect to a pod for interactive use

    Note: If the kubectl command fails, the failure will be printed to stderr by the
    kubectl command and p.wait() will exit immediately.

    Args:
        name: Name of the pod
        context: Kubernetes context in which the pod lives

    Returns:
        True if connection succeeded (after connection is closed) or False if connection closed unexpectedly
    """
    if context.namespace is None:
        raise ValueError('Context must have a valid namespace specified, not None')
    options = f'--context {shlex.quote(context.cluster)} --namespace {shlex.quote(context.namespace)}'
    exec_command = f'kubectl exec -it {options} {name} -- /bin/bash'

    logger.debug(f'Calling: {exec_command}')
    with subprocess.Popen(exec_command, shell=True, start_new_session=True) as p:
        return p.wait() == 0


def get_kube_contexts() -> List[KubeContext]:
    """Returns all configured K8s configured contexts

    Returns:
        List[KubeContext]: A list of the k8s contexts configured.
    """
    raw_contexts = config.list_kube_config_contexts()[0]
    raw_contexts = cast(List[Dict[str, Dict[str, str]]], raw_contexts)
    raw_contexts = [x['context'] for x in raw_contexts]
    contexts = [KubeContext(**x) for x in raw_contexts]
    return contexts


def get_current_context() -> KubeContext:
    """Returns the current K8s context

    Returns:
        KubeContext: The current K8s context
    """
    _, current_context = config.list_kube_config_contexts()

    return KubeContext(**current_context['context'])


# pylint: disable-next=invalid-name
def merge_V1ObjectMeta(*other: client.V1ObjectMeta) -> client.V1ObjectMeta:
    """ Merges a V1ObjectMeta into the Base V1ObjectMeta

    Does not handle lists such as `managed_fields` and `owner_references`

    Returns:
        A new V1ObjectMeta with the merged data
    """
    merged_meta = client.V1ObjectMeta()
    for attr in client.V1ObjectMeta.attribute_map:
        for o in other:
            if getattr(o, attr) is not None:
                found_attr = getattr(o, attr)
                if attr in ('labels', 'annotations') and getattr(merged_meta, attr):
                    base_labels: Dict[str, str] = getattr(merged_meta, attr)
                    base_labels.update(found_attr)
                    setattr(merged_meta, attr, base_labels)
                else:
                    setattr(merged_meta, attr, found_attr)
    return merged_meta


def safe_update_optional_list(
    original_value: Optional[List[Any]],
    additions: List[Any],
) -> List[Any]:
    """ Returns a copy with the merged optional list and additional list """
    if original_value is not None:
        return original_value + additions
    else:
        return copy.deepcopy(additions)


def safe_update_optional_dictionary(
    original_value: Optional[Dict[Any, Any]],
    additions: Dict[Any, Any],
) -> Dict[Any, Any]:
    """ Returns a copy with the merged optional dict and additional dict """
    if original_value is not None:
        new_dict = copy.deepcopy(original_value)
        new_dict.update(additions)
        return new_dict
    else:
        return copy.deepcopy(additions)


@contextmanager
def use_context(context: str) -> Generator[KubeContext, None, None]:
    """_summary_

    Args:
        context (str): Name of the context to use for Kubernetes API calls

    Raises:
        ValueError: if the requested context does not exist

    Yields:
        KubeContext: The KubeContext object for the current context
    """

    poss_contexts = [c for c in get_kube_contexts() if c.cluster == context]
    if len(poss_contexts) == 0:
        raise ValueError(f'No context named {context}')
    new_context = poss_contexts[0]

    previous_context = get_current_context()
    try:
        config.load_kube_config(context=new_context.cluster)
        yield new_context
    finally:
        config.load_kube_config(context=previous_context.cluster)


def base64_encode(message: str, encoding: str = 'utf-8') -> str:
    """Encode the provided message in base64

    Args:
        message (str): Message to encode
        encoding (str, optional): Byte encoding of `message`. Defaults to "utf-8".

    Returns:
        str: base64 encoded `message`
    """
    message_bytes = message.encode(encoding)
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode(encoding)
    return base64_message


def base64_decode(base64_message: str, encoding: str = 'utf-8') -> str:
    """Decode the provided base64-encoded message

    Args:
        base64_message (str): Message encoded in base64 to decode
        encoding (str, optional): Encoding that should be used for resulting message. Defaults to "utf-8".

    Returns:
        str: Decoded message
    """
    base64_bytes = base64_message.encode(encoding)
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode(encoding)
    return message


def kube_call_idem(api_call: Callable, *args, **kwargs) -> Optional[Dict[str, Any]]:
    """Calls the requested API and returns None if the object already exists

    Args:
        api_call: A kubernetes api call
        args, kwargs: Additional *args and **kwargs for the requested API call

    Returns:
        The response if the api call succeeded or None if the object already exists

    Raises:
        Re-raises any ApiExceptions found that weren't due to the object already existing
    """

    try:
        return api_call(*args, **kwargs)
    except client.ApiException as e:
        if not (e.status == 409 and e.reason == 'Conflict'):
            # Error was not a duplicate-name conflict
            raise


def read_secret(name: str, namespace: str) -> Optional[Dict[str, Union[str, Dict[str, Any]]]]:
    """Attempt to read the requested secret

    Args:
        name (str): Name of the secret
        namespace (str): Namespace in which to look

    Returns:
        Optional[Dict[str, str]]: If None, the secret does not exist. Otherwise, the secret is returned as a JSON.
    """
    api = client.CoreV1Api()
    try:
        secret = api.read_namespaced_secret(name=name, namespace=namespace)
        return kube_object_to_dict(secret)
    except client.ApiException:
        return None


def _get_secret_spec(
    name: str,
    data: Dict[str, str],
    secret_type: str = 'Opaque',
    labels: Optional[Dict[str, str]] = None,
    annotations: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Get the Kubernetes spec for the requested secret

    Args:
        name: Name of the secret
        data: Secret data. Should be base64 encoded unless ``encode=True``.
        secret_type: Secret type. Defaults to "Opaque".
        labels: Additional labels that will be added to the secret, if provided.
        annotations: Additional annotations that will be added to the secret, if provided

    Returns:
        bool: True if creation succeeded
    """
    labels = labels or {}
    annotations = annotations or {}

    secret = client.V1Secret(type=secret_type, data=data)
    secret.metadata = client.V1ObjectMeta(name=name, labels=labels, annotations=annotations)
    return kube_object_to_dict(secret)


def create_secret(
    spec: Dict[str, Any],
    namespace: str,
) -> bool:
    """Create the requested secret

    Args:
        spec: Kubernetes spec for the secret
        namespace: Namespace in which the secret should be created

    Returns:
        bool: True if creation succeeded
    """
    api = client.CoreV1Api()
    try:
        api.create_namespaced_secret(namespace=namespace, body=spec)
    except client.ApiException:
        return False
    return True


def update_secret(
    name: str,
    namespace: str,
    data: Dict[str, str],
    labels: Optional[Dict[str, str]] = None,
    annotations: Optional[Dict[str, str]] = None,
) -> bool:
    """Update the requested secret with new data

    Args:
        name (str): Name of the secret
        namespace (str): Namespace in which the secret exists
        data (Dict[str, str]): New secret data. Should be base64 encoded unless ``encode=True``.

    Returns:
        bool: True if update succeeded
    """

    # Get existing secret
    existing_secret = read_secret(name, namespace)
    if not existing_secret:
        raise client.ApiException(f'Could not find a secret named {name} within the namespace {namespace}')
    assert existing_secret is not None
    secret_type = existing_secret['type']

    labels = labels or {}
    annotations = annotations or {}

    api = client.CoreV1Api()
    secret = client.V1Secret(type=secret_type, data=data)
    secret.metadata = client.V1ObjectMeta(name=name, labels=labels, annotations=annotations)
    api.patch_namespaced_secret(name, namespace, body=secret)
    return True


def delete_secret(name: str, namespace: str) -> bool:
    """Delete the requested secret

    Args:
        name: Name of the secret
        namespace: Namespace in which the secret exists

    Returns:
        True if deletion succeeded
    """

    api = client.CoreV1Api()
    try:
        api.delete_namespaced_secret(name, namespace)
    except client.exceptions.ApiException as e:
        logger.debug(f'Failed to delete secret {name} from namespace {namespace}')
        logger.debug(e)
        return False
    return True


def list_secrets(namespace: str, labels: Optional[Dict[str, Optional[str]]] = None) -> Dict[str, Any]:
    """List all secrets in the namespace, filtered by labels

    Args:
        namespace (str): Kubernetes namespace
        labels (Optional[Dict[str, Optional[str]]]): Secret labels that must be matched. Defaults to None.

    Returns:
        Dict[str, Any]: Kubernetes secrets list as a JSON
    """
    if labels is None:
        labels = {}
    label_selector = ','.join([f"{key}{('=' + value) if value else ''}" for key, value in labels.items()])
    api = client.CoreV1Api()
    secrets = api.list_namespaced_secret(namespace=namespace, label_selector=label_selector)
    return kube_object_to_dict(secrets)


def list_jobs(namespace: str, labels: Optional[Dict[str, Optional[str]]] = None) -> Dict[str, Any]:
    if labels is None:
        labels = {}
    label_selector = ','.join([f"{key}{('=' + value) if value else ''}" for key, value in labels.items()])
    api = client.BatchV1Api()
    jobs = api.list_namespaced_job(namespace=namespace, label_selector=label_selector)
    return kube_object_to_dict(jobs)


def list_jobs_across_contexts(contexts: List[KubeContext],
                              labels: Optional[Dict[str, Optional[str]]] = None,
                              async_req: bool = True) -> List[Dict[str, Any]]:
    if labels is None:
        labels = {}
    label_selector = ','.join([f"{key}{('=' + value) if value else ''}" for key, value in labels.items()])
    job_requests = []
    for context in contexts:
        if context.namespace is None:
            print(f'No namespace for context {context.cluster}')
            continue
        with use_context(context.cluster):
            api = client.BatchV1Api()
            job_request = api.list_namespaced_job(namespace=context.namespace,
                                                  label_selector=label_selector,
                                                  async_req=async_req)
            job_requests.append(job_request)
    all_jobs = []
    for req in job_requests:
        jobs = req.get() if async_req else req
        all_jobs.extend(kube_object_to_dict(jobs)['items'])
    return all_jobs


class LogParseError(Exception):
    """Exception raised when workload logs cannot be properly parsed
    """


# pylint: disable=redefined-outer-name
def get_pod_logs(name: str, namespace: str, logger: Optional[logging.Logger] = None) -> List[str]:
    """Stream the logs for the requested pod and return them as a list of log lines

    Arguments:
        name: Pod name
        namespace: Namespace in which the pod lives
        logger: Optional logger that lines will be sent to. Lines are logged under
            logging.INFO level. If not provided, lines will be printed instead.

    Returns:
        List of log lines

    Raises:
        LogParseError: Raised if the logs were returned from Kubernetes but could not be parsed.
    """
    v1 = client.CoreV1Api()
    w = watch.Watch()
    logs = []
    try:
        for line in w.stream(v1.read_namespaced_pod_log, name=name, namespace=namespace):
            logs.append(line)
            if logger is not None:
                logger.info(line)
            else:
                print(line)
    except UnicodeDecodeError as e:
        kubectl_cmd = f'kubectl -n {namespace} logs {name}'
        raise LogParseError(
            'Error occurred while attempting to parse workload logs. This is likely due to a bug in the Kubernetes '
            f'python API. If you have `kubectl` installed, you can try viewing logs using {kubectl_cmd}') from e

    return logs


class PodStatusEpilog():
    """Callbacks for printing pod status using ``rich`` status messages
    """

    def __init__(self, rich_status):
        self.status = rich_status

    def __call__(self, event: PodEvent):
        logger.debug(str(event))
        if event.status == 'Scheduled':
            self.status.update('Pulling Docker image...')
        elif event.status == 'FailedScheduling':
            self.status.update('Failed scheduling: insufficient resources. Trying again...')
        elif event.status == 'Pulled':
            self.status.update('Workload starting...')
        elif event.status == 'Started':
            raise StopWatching
