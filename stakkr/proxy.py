"""
Manage public proxy to expose containers
"""

import os
from docker.errors import DockerException
from stakkr import docker_actions
from stakkr.configreader import Config


class Proxy():
    """Main class that does actions asked in the cli"""

    def __init__(self, port: int = 80, proxy_name: str = 'proxy_stakkr'):
        """Set the right values to start the proxy"""

        self.port = port
        self.proxy_name = proxy_name
        self.docker_client = docker_actions.get_client()

    def start(self, stakkr_network: str):
        """Start stakkr proxy if stopped"""

        if docker_actions.container_running(self.proxy_name) is True:
            return

        api_client = docker_actions.get_api_client()
        # Start the CT
        try:
            self.docker_client.containers.run(
                'traefik', remove=True, detach=True, hostname=self.proxy_name,
                name=self.proxy_name, command='--api --docker',
                volumes=['/var/run/docker.sock:/var/run/docker.sock'],
                ports={80: self.port, 8080: 8080})
        except DockerException as error:
            raise RuntimeError("Can't start proxy ...")

        # Connect it to the main network
        docker_actions.add_container_to_network(self.proxy_name, stakkr_network)


    def stop(self):
        """Stop stakkr proxy"""

        if docker_actions.container_running(self.proxy_name) is False:
            return

        self.docker_client.containers.get(self.proxy_name).stop()
