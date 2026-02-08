
# Includes and Imports
from typing import List
from pathlib import Path
import os
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse
import uvicorn
from pydantic import BaseModel
import docker
from app.config import SERVICE_DEFS
from app.helpers import get_containers_by_name, build_service_states, check_pihole
from app.models import DockerContainer


# Create app
api = FastAPI(title="API", docs_url="/docs", openapi_url="/openapi.json")
app = FastAPI(title="Server Dashboard API", version="1.0.0")

docker_client = docker.from_env()

FRONTEND_DIST = "/app/frontend/dist"

app.mount("/api", api)
app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")



class Container(BaseModel):
    name: str
    id: str
    status: str
    health: str

class Service(BaseModel):
    id: str
    name: str
    group: str
    is_docker: bool = False
    url: str | None
    url_status: str | None
    service_status: str
    container: DockerContainer | None


@api.get("/health")
def health():
    try:
        docker_client.info()
        return {"status": "ok"}
    except Exception as error:
        return {"status": "error", "message": str(error)}


# Define get_services endpoint - gets list of services
@api.get("/services", response_model=List[Service])
def get_services():
    containers_by_name = get_containers_by_name()
    states = build_service_states(SERVICE_DEFS.values())
    result: list[Service] = []

    for svc_state in states:
        service = svc_state.service
        container_out: DockerContainer | None = None 

        if service.is_docker and service.container_name:
            container_obj = containers_by_name.get(service.container_name)
            if container_obj:
                container_out = DockerContainer(
                    name=container_obj.name,
                    id=container_obj.id,
                    status=container_obj.status,
                )
        
        url_status = svc_state.url_status.value if svc_state.url_status is not None else None

        result.append(
            Service(
                id=service.id,
                name=service.name,
                group=service.group,
                is_docker=service.is_docker,
                url=service.url,
                url_status=url_status,
                service_status=svc_state.service_status.value,
                container=container_out,
            )
        )
    return result




# Define restart_service endpoint - restarts a docker container service
@api.post("/services/{service_id}/restart")
def restart_service(service_id: str):

    service = SERVICE_DEFS.get(service_id)

    if not service:
        raise HTTPException(status_code=404, detail="Service not in config")

    if not service.is_docker:
        raise HTTPException(status_code=400, detail="Restart only supported for docker services")

    # attempt to get container by container_name and restart it
    try:
        container = docker_client.containers.get(service.container_name)
        container.restart()

    # handle exceptions - service not found
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Docker container not found")
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Failed to restart: {error}")

    return {
        "status": "restarted",
        "service_id": service_id,
        "container_name": service.container_name,
    }


