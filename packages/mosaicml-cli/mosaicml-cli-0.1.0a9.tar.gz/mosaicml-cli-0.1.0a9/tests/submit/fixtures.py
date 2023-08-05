import copy
import os
import tempfile

import pytest
import yaml

from mcli.serverside.platforms.registry import PlatformRegistry


@pytest.fixture
def platform_registry() -> PlatformRegistry:
    with tempfile.TemporaryDirectory() as tmpdirname:

        # Fake kubeconfig
        tmp_kubeconfig = tmpdirname + '/kubeconfig'
        os.environ['KUBECONFIG'] = tmp_kubeconfig
        with open(tmp_kubeconfig, 'w') as f:
            context = {
                'cluster': 'test-cluster',
                'namespace': 'test-user',
                'user': 'test-user',
            }

            yaml.dump(
                {
                    'apiVersion': 'v1',
                    'clusters': [{
                        'cluster': {
                            'server': 'https://foobar'
                        },
                        'name': 'test-cluster'
                    }],
                    'contexts': [{
                        'name': 'aws-research-01',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'azure-research-01',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'gcp-research-01',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'colo-research-01',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'r1z1',
                        'context': copy.deepcopy(context),
                    }, {
                        'name': 'r6z1',
                        'context': copy.deepcopy(context),
                    }],
                    'current-context': 'aws-research-01'
                }, f)

        with open(os.environ['KUBECONFIG'], 'r') as f:
            print(f.read())

        return PlatformRegistry()
