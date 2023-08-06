# pylint: disable=duplicate-code

""" Helper folder to load Platform from Configs """
import json
import os

from kubernetes import config as kubectl_get_contexts

from mcli import config


class NamespaceConfigError(Exception):
    pass


def get_platform_config(config_file=None):
    """
    Loads the platform config from `~/.mosaic/config` or
    MOSAICCONFIG environment variables.
    """
    if config_file is None:
        config_file = config.MCTL_CONFIG_PATH

    if isinstance(config_file, dict):
        platform_config = config_file
    elif os.path.isfile(config_file):
        with open(config_file, 'r', encoding='utf8') as f:
            platform_config = json.load(f)
    else:
        raise ValueError(f'{config_file} not found. Config file '
                         'should be in ~/.mosaic/config or location '
                         'set by the MOSAICCONFIG environment variable.')

    return platform_config


def verify_config_namespaces(platform_config: dict):
    """
    Verify that the kube config file has namespaces configured, and that the
    namespaces match that in the mosaic config.
    """

    contexts, _ = kubectl_get_contexts.list_kube_config_contexts()

    for _, platform in platform_config.items():

        context_config = [c for c in contexts if c['name'] == platform['context_name']]
        if len(context_config) == 0:
            raise ValueError(f'Did not find context {platform["context_name"]} in kube config file.')

        context_config = context_config[0]['context']

        if 'namespace' not in context_config:
            raise NamespaceConfigError(f'No namespace found in kube config for {platform["context_name"]}.')
        elif context_config['namespace'] != platform['namespace']:
            config_namespace = context_config['namespace']
            raise NamespaceConfigError(f'In context {platform["context_name"]}, expected '
                                       f'namespace {platform["namespace"]} but kube config '
                                       f'has namespace {config_namespace}. Please fix with kubectl.')
