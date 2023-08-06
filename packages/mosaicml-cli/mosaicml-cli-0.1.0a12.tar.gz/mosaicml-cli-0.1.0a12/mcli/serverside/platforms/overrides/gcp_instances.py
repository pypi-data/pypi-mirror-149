""" GCP Available Instances """

from mcli.serverside.job.mcli_k8s_job_typing import MCLIK8sResourceRequirements
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.platform_instances import CloudPlatformInstances, InstanceTypeLookupData
from mcli.utils.utils_kube_labels import label

a100_g4_instance = InstanceType(
    gpu_type=GPUType.A100_40GB,
    gpu_num=4,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=48,
        memory=340,
        storage=80,
    ),
    selectors={
        label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.GCP_A100_4G,
    },
)

a100_g8_instance = InstanceType(
    gpu_type=GPUType.A100_40GB,
    gpu_num=8,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=96,
        memory=680,
        storage=80,
    ),
    selectors={
        label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.GCP_A100_8G,
    },
)
a100_g16_instance = InstanceType(
    gpu_type=GPUType.A100_40GB,
    gpu_num=16,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=96,
        memory=1360,
        storage=80,
    ),
    selectors={
        label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.GCP_A100_16G,
    },
)

v100_g8_instance = InstanceType(
    gpu_type=GPUType.V100_16GB,
    gpu_num=8,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=64,
        memory=416,
        storage=80,
    ),
    selectors={
        label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.GCP_V100_8G,
    },
)
GCP_ALLOWED_INSTANCES = CloudPlatformInstances(instance_type_map={
    InstanceTypeLookupData(GPUType.A100_40GB, 4): a100_g4_instance,
    InstanceTypeLookupData(GPUType.A100_40GB, 8): a100_g8_instance,
    InstanceTypeLookupData(GPUType.A100_40GB, 16): a100_g16_instance,
    InstanceTypeLookupData(GPUType.V100_16GB, 8): v100_g8_instance,
},)
