# pylint: disable=duplicate-code

""" The InstanceList of allowed AWS InstanceTypes """

from mcli.serverside.platforms.instance_type import GPUType, InstanceList, InstanceType

ALLOWED_INSTANCES = [
    InstanceType(
        name='c5.large',
        cpu_count=2,
        gpu_count=0,
        gpu_type=GPUType.NONE,
        desc='Lightweight instance',
    ),
    InstanceType(
        name='c5.2xlarge',
        cpu_count=8,
        gpu_count=0,
        gpu_type=GPUType.NONE,
        desc='CLX/SKX Xeon CPU',
    ),
    InstanceType(
        name='c5.9xlarge',
        cpu_count=36,
        gpu_count=0,
        gpu_type=GPUType.NONE,
        desc='CLX/SKX Xeon CPU',
    ),
    InstanceType(
        name='c5.24xlarge',
        cpu_count=96,
        gpu_count=0,
        gpu_type=GPUType.NONE,
        desc='CLX/SKX Xeon CPU',
    ),
    InstanceType(
        name='p2.xlarge',
        cpu_count=4,
        gpu_count=1,
        gpu_type=GPUType.K80,
        gpu_memory=12,
        desc='1x K80 GPU (12GB)',
    ),
    InstanceType(
        name='p2.8xlarge',
        cpu_count=32,
        gpu_count=8,
        gpu_type=GPUType.K80,
        gpu_memory=12,
        desc='8x K80 GPU (12GB)',
    ),
    InstanceType(
        name='p3.2xlarge',
        cpu_count=8,
        gpu_count=1,
        gpu_type=GPUType.V100,
        gpu_memory=16,
        desc='1x V100 GPU (16GB)',
    ),
    InstanceType(
        name='g4dn.2xlarge',
        cpu_count=8,
        gpu_count=1,
        gpu_type=GPUType.T4,
        gpu_memory=16,
        desc='1x T4 GPU (16GB)',
    ),
    InstanceType(
        name='g4dn.12xlarge',
        cpu_count=48,
        gpu_count=4,
        gpu_type=GPUType.T4,
        gpu_memory=16,
        desc='4x T4 GPU (16GB)',
    ),
    InstanceType(
        name='g4dn.metal',
        cpu_count=96,
        gpu_count=8,
        gpu_type=GPUType.T4,
        gpu_memory=16,
        desc='8x T4 GPU (16GB)',
    ),
    InstanceType(
        name='p3.16xlarge',
        cpu_count=64,
        gpu_count=8,
        gpu_type=GPUType.V100,
        gpu_memory=16,
        desc='8x V100 GPU w/ NVLink (16GB)',
    ),
    InstanceType(
        name='p3dn.24xlarge',
        cpu_count=96,
        gpu_count=8,
        gpu_type=GPUType.V100,
        gpu_memory=32,
        desc='8x V100 GPU w/ NVLink (32GB)',
    ),
    InstanceType(
        name='p4d.24xlarge',
        cpu_count=96,
        gpu_count=8,
        gpu_type=GPUType.A100,
        gpu_memory=40,
        desc='8x A100 GPU w/ NVLink (40GB)',
    ),
]

AWS_INSTANCE_LIST = InstanceList(instances=ALLOWED_INSTANCES)
