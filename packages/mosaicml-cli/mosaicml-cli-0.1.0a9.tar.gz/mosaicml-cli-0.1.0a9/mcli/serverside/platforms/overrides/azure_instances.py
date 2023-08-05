# pylint: disable=duplicate-code

""" The InstanceList of allowed Azure InstanceTypes """
from mcli.serverside.platforms.instance_type import GPUType, InstanceList, InstanceType

ALLOWED_INSTANCES = [
    InstanceType(
        name='Standard_B2s',
        cpu_count=2,
        gpu_count=0,
        desc='Lightweight VM',
    ),
    InstanceType(
        name='Standard_F72s_v2',
        cpu_count=7,
        gpu_count=0,
        desc='Heavyweight CPU-Only VM',
    ),
    InstanceType(
        name='Standard_NC6_Promo',
        cpu_count=6,
        gpu_count=1,
        gpu_type=GPUType.K80,
        gpu_memory=12,
        desc='1x K80 GPU (12GB)',
    ),
    InstanceType(
        name='Standard_NC12_Promo',
        cpu_count=1,
        gpu_count=2,
        gpu_type=GPUType.K80,
        gpu_memory=12,
        desc='2x K80 GPU (12GB)',
    ),
    InstanceType(
        name='Standard_NC6s_v2',
        cpu_count=6,
        gpu_count=1,
        gpu_type=GPUType.P100,
        gpu_memory=16,
        desc='1x P100 GPU (16GB)',
    ),
    InstanceType(
        name='Standard_NC6s_v3',
        cpu_count=6,
        gpu_count=1,
        gpu_type=GPUType.V100,
        gpu_memory=16,
        desc='1x V100 GPU (16GB)',
    ),
    InstanceType(
        name='Standard_NC24s_v3',
        cpu_count=2,
        gpu_count=4,
        gpu_type=GPUType.V100,
        gpu_memory=16,
        desc='4x V100 GPU (16GB)',
    ),
    InstanceType(
        name='Standard_NC4as_T4_v3',
        cpu_count=4,
        gpu_count=1,
        gpu_type=GPUType.T4,
        gpu_memory=16,
        desc='1x T4 GPU (16GB)',
    ),
    InstanceType(
        name='Standard_NC8as_T4_v3',
        cpu_count=8,
        gpu_count=1,
        gpu_type=GPUType.T4,
        gpu_memory=16,
        desc='1x T4 GPU (16GB)',
    ),
    InstanceType(
        name='Standard_NC64as_T4_v3',
        cpu_count=6,
        gpu_count=4,
        gpu_type=GPUType.T4,
        gpu_memory=16,
        desc='4x T4 GPU (16GB)',
    ),
    InstanceType(
        name='Standard_ND96asr_v4',
        cpu_count=9,
        gpu_count=8,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='8x A100 GPU (40GB)',
    ),
]

AZURE_INSTANCE_LIST = InstanceList(instances=ALLOWED_INSTANCES)
