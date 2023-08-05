""" mcli init_kube Entrypoint """
import logging
import textwrap
from typing import Optional

from mcli.config import MCLI_KUBECONFIG
from mcli.utils.utils_interactive import list_options
from mcli.utils.utils_logging import FAIL, OK, console
from mcli.utils.utils_rancher import configure_namespaces, generate_cluster_config, retrieve_clusters, retrieve_projects

DEFAULT_RANCHER_ENDPOINT = 'https://rancher.z0.r0.mosaicml.cloud'

logger = logging.getLogger(__name__)


def initialize_k8s(
    auth_token: Optional[str] = None,
    rancher_endpoint: Optional[str] = None,
    namespace: Optional[str] = None,
    **kwargs,
) -> int:
    del kwargs

    # Get required info
    if not auth_token:
        auth_token = list_options(
            input_text='What is your Rancher API key?',
            options=[],
            allow_custom_response=True,
            multiple_ok=False,
            pre_helptext='',
            helptext='Also called the "bearer token" when creating a new API key',
            print_response=False,
        )

    assert auth_token is not None

    if not rancher_endpoint:
        rancher_endpoint = list_options(
            input_text='Which Rancher endpoint URL is this?',
            options=[],
            allow_custom_response=True,
            multiple_ok=False,
            pre_helptext='',
            helptext=f'The Rancher URL, including https. Default: {DEFAULT_RANCHER_ENDPOINT}',
            print_response=False,
            default_response=DEFAULT_RANCHER_ENDPOINT,
        )

    assert rancher_endpoint is not None
    # Ensure no trailing '/'. Didn't add as a validator because it's annoying for the end user
    rancher_endpoint = rancher_endpoint.rstrip('/')

    if not namespace:
        namespace = list_options(
            input_text='What should your namespace be?',
            options=[],
            allow_custom_response=True,
            multiple_ok=False,
            pre_helptext='',
            helptext='The namespace you would like created or were given',
            print_response=False,
        )

    assert namespace is not None

    try:
        # Retrieve all available clusters
        with console.status('Retrieving clusters...'):
            clusters = retrieve_clusters(rancher_endpoint, auth_token)
        if clusters:
            logger.info(f'{OK} Found {len(clusters)} clusters that you have access to')
        else:
            logger.error(f'{FAIL} No clusters found. Please double-check that you have access to clusters in Rancher')
            return 1

        # Setup namespace
        with console.status('Getting available projects...'):
            projects = retrieve_projects(rancher_endpoint, auth_token)
        with console.status(f'Setting up namespace {namespace}...'):
            configure_namespaces(rancher_endpoint, auth_token, clusters, projects, namespace)
        logger.info(f'{OK} Configured namespace {namespace} in {len(clusters)} available clusters')

        # Generate kubeconfig file from clusters
        with console.status('Generating custom kubeconfig file...'):
            generate_cluster_config(rancher_endpoint, auth_token, clusters, namespace)
        logger.info(f'{OK} Created a new Kubernetes config file at: {MCLI_KUBECONFIG}')

        # Suggest next steps
        cluster_names = ', '.join(cluster.name for cluster in clusters)
        logger.info(f'You now have access to [bold green]{len(clusters)}[/] new clusters: '
                    f'[bold green]{cluster_names}[/]')
        logger.info(
            textwrap.dedent(f"""
                To use these, you\'ll first need to include them in your KUBECONFIG environment variable. For example,
                you can add this line to your ~/.bashrc or ~/.zshrc file:

                [bold]export KUBECONFIG=$KUBECONFIG:{MCLI_KUBECONFIG}[/]


                Once you've done that, add any new clusters you want to use in `mcli` using:

                [bold]mcli create platform <CLUSTER>[/]

                where <CLUSTER> is any of the cluster names above.
                """))

    except RuntimeError as e:
        logger.error(f'{FAIL} {e}')
        return 1

    return 0
