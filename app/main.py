
# Includes and Imports
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import yaml
import docker
import http.client, urllib.parse


# Base Service Model
class Service(BaseModel):
    id: str                                 # used to id services for API's
    name: str                               # self defined service name
    container_name: Optional[str] = None    # container name (as defined is synology container manager or docker)
    url: str | None = None                  # url for service
    group: str                              # group for service  ('monitoring', 'dev', 'media', etc.)
    type: str                               # type of service ('app' or 'docker' container)
    status: str | None = None               # status of service (up or down)
    

# Set the config path and define dictionary for services
CONFIG_PATH = Path("/app/config.yaml")
SERVICE_DEFS: dict[str, Service] = {}


# Create app
app = FastAPI(title="Server Dashboard API", version="1.0.0")

# Set docker_client from the environment
docker_client = docker.from_env()



# Define load_config function   
def load_config() -> None:

    # use global version, instead of new local variable
    global SERVICE_DEFS

    # if the config path doesn't exist, set dict to {} and return
    if not CONFIG_PATH.exists():
        SERVICE_DEFS = {}
        return

    # open config path and read config file with safe open
    with CONFIG_PATH.open("r") as config:
        raw = yaml.safe_load(config) or {}
    
    # create raw services from yaml config file
    services = raw.get("services", [])

    # maps container_name -> service object
    SERVICE_DEFS = {}

    # assign each yaml service to dictionary
    for item in services:
        svc = Service(
            id=item["id"],
            name=item["name"],
            container_name=item.get("container_name"),
            status=None,
            url=item.get("url"),
            group=item.get("group"),
            type=item.get("type", "docker"),
        )
        SERVICE_DEFS[svc.id] = svc

load_config()

#  end of load_config function



@app.get("/health")
def health():
    try:
        docker_client.ping()
        return {"status": "ok"}
    except Exception as error:
        return {"status": "error", "message": str(error)}


# Define get_services endpoint - gets list of services
@app.get("/services", response_model=List[Service])
def get_services():

    # get list of all containers
    containers = docker_client.containers.list(all=True)

    # map container IDs to container objects for quick lookup
    containers_by_name = {container.name: container for container in containers}

    # prepare result list
    result: list[Service] = []

    # cycle through each service definition and retrieve values
    for svc in SERVICE_DEFS.values():

        # default status to unknown
        status = "unknown"

        # if type is docker, get container status  (id must be same as container name)
        if svc.type == "docker":
            container = containers_by_name.get(svc.id)    
            status = container.status if container is not None else "not_found"

        # if type is app, check url status
        elif svc.type == "app" and svc.url:
            try:
                parsedURL = urllib.parse.urlparse(svc.url)
                port = parsedURL.port or (443 if parsedURL.scheme == "https" else 80)
                connection_class = http.client.HTTPSConnection if parsedURL.scheme == "https" else http.client.HTTPConnection
                connection = connection_class(parsedURL.hostname, port, timeout=2)
                connection.request("GET", parsedURL.path or "/")
                response = connection.getresponse()
                status = "up" if response.status < 500 else "down"
            except Exception:
                status = "down"
    
        # append service to result list
        result.append(
            Service(
                id=svc.id,
                name=svc.name,
                container_name=svc.container_name,
                status=status,
                url=svc.url,
                group=svc.group,
                type=svc.type,
            )
        )

    return result


# Define restart_service endpoint - restarts a docker container service
@app.post("/services/{service_id}/restart")
def restart_service(service_id: str):

    service = SERVICE_DEFS.get(service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not in config")
    
    if service.type != "docker":
        raise HTTPException(status_code=400, detail="Restart only supported for docker services")

    # attempt to get container by service_id and restart it
    try:
        container = docker_client.containers.get(service_id)
        container.restart()
    
    # handle exceptions - service not found
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Docker container not found")
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Failed to restart: {error}")

    return {"status": "restarted", "service_id": service_id}    

