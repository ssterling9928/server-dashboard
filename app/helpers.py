from typing import Iterable
import docker
import requests
from app.models import ContainerStatus, DockerContainer, ServiceState, URLStatus, ServiceStatus, ServiceConfig

containers_by_name = {}
docker_client = docker.from_env()

def get_containers_by_name() -> dict[str, 'docker.models.containers.Container']:
    
    containers = docker_client.containers.list(all=True)
    
    by_name: dict[str, 'docker.models.containers.Container'] = {}
    for container in containers:
        by_name[container.name] = container 
    
    return by_name



def check_pihole():

    cont = docker_client.containers.get("pihole")

    result = cont.exec_run("curl -fsS http://localhost/admin/", privileged=True)
    exit_code = result.exit_code  

    return URLStatus.UP if exit_code == 0 else URLStatus.WARN



def check_url_status(url: str | None, timeout: float = 2) -> URLStatus:

    internal = ".internal" in url

    try:
        resp = requests.get(url, timeout=timeout, verify=not internal)
        return URLStatus.UP if resp.status_code < 400 else URLStatus.WARN
    except requests.exceptions.Timeout:
        return URLStatus.TIMEOUT
    except requests.exceptions.RequestException as e:
        print(f"Check {url}: {e}")  # Debug
        return URLStatus.UNREACHABLE



def build_service_states(services: Iterable[ServiceConfig]) -> list[ServiceState]:

    states: list[ServiceState] = []
    containers = get_containers_by_name()

    for svc in services:
 
        container_status: ContainerStatus | None = None
        url_status: URLStatus | None = None
        service_status: ServiceStatus

        # Set container_status if service has a container
        if svc.is_docker and svc.container_name is not None:
            container = containers.get(svc.container_name)
            if container:
                container_status = container.status

        
        # Set url_status if service has a URL
        if svc.id == "pihole":
            url_status = check_pihole()
        elif svc.url is not None:
            url_status = check_url_status(svc.url)



        # Has Container | Has URL
        if container_status is not None and url_status is not None:
            if container_status == ContainerStatus.RUNNING and url_status == URLStatus.UP:
                service_status = ServiceStatus.OK
            else:
                service_status = ServiceStatus.DEGRADED


        # Has Container | No URL  
        elif container_status is not None and url_status is None:
            if container_status == ContainerStatus.RUNNING:
                service_status = ServiceStatus.OK
            else:
                service_status = ServiceStatus.DEGRADED

        # No Container | Has URL
        elif container_status is None and url_status is not None:
            if url_status == URLStatus.UP:
                service_status = ServiceStatus.OK
            if url_status == URLStatus.DOWN:
                service_status = ServiceStatus.DOWN

        else:
            service_status = ServiceStatus.UNKNOWN

        states.append(
            ServiceState(
                service = svc,
                container_status=container_status,
                url_status=url_status,
                service_status=service_status,
            )
        )

    return states
