
# Includes and Imports
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List
from pathlib import Path
import yaml
import docker
import http.client, urllib.parse

# Set the config path and define dictionary for services
CONFIG_PATH = Path("/app/config.yaml")
SERVICE_DEFS: dict[str, Service] = {}

# Create app
app = FastAPI(title="Server Dashboard API", version="1.0.0")

# Set docker_client from the environment
docker_client = docker.from_env()

# Base Service Model
class Service(BaseModel):
    id: str                                 # used to id services for API's
    name: str                               # self defined service name
    container_name: Optional[str] = None    # container name (as defined is synology container manager or docker)
    url: str | None = None                  # url for service
    group: str                              # group for service  ('monitoring', 'dev', 'media', etc.)
    type: str                               # type of service ('app' or 'docker' container)
    status: str | None = None               # status of service (up or down)
    

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
        raw = yaml.safe_open(config) or {}
    
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
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/services", response_model=List[Service])
def get_services():
    containers = docker_client.containers.List(all=True)
    containers_by_id = {container.id: container for container in containers}

    result: list[Service] = []
    for svc in SERVICE_DEFS.values():
        if svc.type == "docker" and svc.container_name:
            container = containers_by_name.get(svc.container_name)
            status = container.status if container is not None else "not_found"
        elif svc.type == "app" and svc.url:
            try:
                parsedURL = urllib.parse.urlparse(svc.url)
                port = parsed.port or (443 if parsed.scheme == "https" else 80)
                connection_class = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
                connection = connection_class(parsedURL.hostname, port, timeout=2)
                connection.request("GET", parsedURL.path or "/")
                response = connection.response()
                status = "up" if resp.status < 500 else "down"
            except Exception:
                status = "down"
    result.append(
        Service(
            name=svc.name,
            container_name=svc.container_name,
            status=svc.status,
            url=svc.url,
            group=svc.group,
            type=svc.type,
        )
    )

    return result


@app.post("/services/{container_name}/restart")
def restart_service(service_id: str):
    try:
        container = docker_client.containers.get(service_id)
        container.restart()
        return {"status": "restarted", "service_id": service_id}
    except docker.errors.NotFound:
        return {"status": "error", "message": "Service not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

