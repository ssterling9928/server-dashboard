from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import docker 

app = FastAPI(title="Server Dashboard API", version="1.0.0")

docker_client = docker.from_env()

class Service(BaseModel):
    id: str
    name: str
    status: str
    url: str | None = None

@app.get("/health")
def health():
    try:
        docker_client.ping()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/services", response_model=List[Service])
def get_services():
    services = []
    for container in docker_client.containers.list(all=True):
        service = Service(
            id=container.id,
            name=container.name,
            status=container.status,
            url=None  # Placeholder for URL, can be populated based on service config
        )
        services.append(service)
    return services

@app.post("/services/{service_id}/restart")
def restart_service(service_id: str):
    try:
        container = docker_client.containers.get(service_id)
        container.restart()
        return {"status": "restarted", "service_id": service_id}
    except docker.errors.NotFound:
        return {"status": "error", "message": "Service not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

