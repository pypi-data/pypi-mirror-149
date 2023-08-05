""" Label Holders """
from __future__ import annotations


class PrefixMetaclass(type):
    """ Modifies all attributes of a class to append a prefix keyed 'prefix'"""

    def __new__(cls, clsname, bases, attrs):
        assert 'prefix' in attrs
        prefix = attrs['prefix']
        del attrs['prefix']
        prefixed_items = {}
        for k, v in attrs.items():
            if isinstance(v, str):
                if prefix != '':
                    prefixed_items[k] = f'{prefix}/{v}'
                else:
                    prefixed_items[k] = v
            else:
                prefixed_items[k] = v
        return type.__new__(cls, clsname, bases, prefixed_items)


class CotaLabelHolder(object, metaclass=PrefixMetaclass):
    prefix = 'mosaicml.com'

    PREFER_GPU_WORKLOADS = 'prefer-gpu-workloads'
    MULTIGPU_8 = 'multigpu_8'


class MosaicCloudHolder(object, metaclass=PrefixMetaclass):
    prefix = 'mosaicml.cloud'

    INSTANCE_SIZE = 'instance-size'


class MosaicInstanceSizeHolder(object, metaclass=PrefixMetaclass):
    """ Special mosaicml.cloud/instance-size Label holder

    Stores our cloud defined instance-size labels with no prefix
    to use within our codebase
    """

    prefix = ''

    A100_80G_1 = 'mosaic.a100-80sxm.1'
    A100_80G_2 = 'mosaic.a100-80sxm.2'  # unused for now
    A100_40G_1 = 'mosaic.a100-40sxm.1'
    OCI_G4_8 = 'oci.bm.gpu4.8'


class MosaicLabelHolder(object, metaclass=PrefixMetaclass):
    """ Base Mosaic Labels """
    prefix = 'mosaicml.com'

    JOB = 'job'

    NODE_CLASS = 'node-class'

    LABEL_INSTANCE = 'instance'
    LABEL_SWEEP = 'sweep'

    # Cloud Labels
    cloud = MosaicCloudHolder

    # Cloud Instance-Size Labels
    instance_size_types = MosaicInstanceSizeHolder

    # Cota Labels
    cota = CotaLabelHolder

    # MCLI Version
    MCLI_VERSION = 'mcli_version'
    MCLI_VERSION_MAJOR = 'mcli_version_major'
    MCLI_VERSION_MINOR = 'mcli_version_minor'
    MCLI_VERSION_PATCH = 'mcli_version_patch'

    LAUNCHER_TYPE = 'launcher_type'

    # Secrets
    SECRET_TYPE = 'secret-type'


class KubernetesNodeLabelHolder(object, metaclass=PrefixMetaclass):
    prefix = 'node.kubernetes.io'

    INSTANCE_TYPE = 'instance-type'


class NvidiaLabelHolder(object, metaclass=PrefixMetaclass):
    prefix = 'nvidia.com'

    GPU = 'gpu'


class LabelHolder():
    mosaic = MosaicLabelHolder
    nvidia = NvidiaLabelHolder
    kubernetes_node = KubernetesNodeLabelHolder


label = LabelHolder
