from time import sleep
from typing import Union

import docker
import docker.errors
from docker.models.secrets import Secret
from docker.models.services import Service
from docker.types import SecretReference

from edos.exceptions import UserReadableException
from edos.exceptions.do_custom import SecretDoesNotExists
from edos.settings import conf


class DockerService:
    def __init__(self):
        self.client = docker.DockerClient(base_url=conf.DOCKER_BASE_URL, use_ssh_client=True)

    def get_node_name_for_service(self, service_name) -> Union[str, None]:
        services = self.client.services.list(filters={"name": service_name})
        if not services or services[0].name != service_name:
            raise UserReadableException("No service found")
        tasks = services[0].tasks(filters={"desired-state": "running"})
        if not tasks:
            raise UserReadableException("No running tasks for this service")
        node_id = tasks[0]["NodeID"]
        return self.client.nodes.get(node_id).attrs.get("Description").get("Hostname")

    def get_container(self, hostname, service_name):
        client = docker.DockerClient(base_url=f"ssh://{hostname}", use_ssh_client=True)
        services = self.client.services.list(filters={"name": service_name})
        if not services or services[0].name != service_name:
            raise UserReadableException("No service found")
        return client.containers.list(filters={"label": [f"com.docker.swarm.service.id={services[0].id}"]})[0].name

    def get_services(self) -> list[Service]:
        return self.client.services.list()

    def get_secrets(self) -> list[Secret]:
        return self.client.secrets.list()

    def create_secret(self, name: str, secret_data: bytes) -> Secret:
        """Create a secret, returning Secret object"""
        try:
            return self.client.secrets.create(name=name, data=secret_data)
        except docker.errors.APIError as exc:
            raise UserReadableException(f"Error when creating secret: {exc.response.reason}")

    def remove_secret(self, name: str):
        """Remove a secret"""
        try:
            self.client.secrets.get(name).remove()
        except docker.errors.NotFound:
            raise UserReadableException("Secret not found")
        except docker.errors.APIError as exc:
            raise UserReadableException(f"Error when removing secret: {exc.response.reason}")

    def get_old_secret(self, secret_name: str):
        self.client.services.create(
            image="apline",
            secrets=[
                secret_name,
            ],
            command=f"cat /run/secrets/{secret_name}",
        )

    def get_secret_by_name(self, secret_name: str):
        secrets = self.client.secrets.list(filters={"name": secret_name})
        if not secrets or secrets[0].name != secret_name:
            raise SecretDoesNotExists("No such secret")
        return secrets[0]

    def create_service_with_secret(self, secret: Secret):
        secret_ref = SecretReference(secret_name=secret.name, secret_id=secret.id)
        return self.client.services.create(
            image="alpine",
            secrets=[
                secret_ref,
            ],
            command="tail -f /dev/null",
            constraints=[f"node.hostname=={conf.DOCKER_MAIN_SWARM_HOSTNAME}"],
        )

    def get_container_name_by_service(self, service: Service) -> str:
        container_name = None
        i = 0
        while i != 10:
            sleep(1)
            try:
                container_name = self.client.containers.list(
                    filters={"label": [f"com.docker.swarm.service.id={service.id}"]}
                )[0].name
                return container_name
            except IndexError:
                i = i + 1
        if not container_name:
            raise UserReadableException("Timeout")

    def get_services_without_reservation(self) -> list[Service]:
        services = self.client.services.list()
        services_without_reservation: list[Service] = []
        for service in services:
            try:
                service.attrs["Spec"]["TaskTemplate"]["Resources"]["Reservations"]["MemoryBytes"]
            except KeyError:
                services_without_reservation.append(service)
        return services_without_reservation
