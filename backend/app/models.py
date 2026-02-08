from typing import Optional
from dataclasses import dataclass
from enum import Enum


class ContainerStatus(str, Enum):
    UNKNOWN = "unknown"
    RUNNING = "running"
    EXITED = "exited"
    RESTARTING = "restarting"
    PAUSED = "paused"

class ServiceStatus(str, Enum):
    UNKNOWN = "unknown"
    OK = "ok"
    DEGRADED = "degraded"
    DOWN = "down"

class URLStatus(str, Enum):
    UNKNOWN = "unknown"
    UP = "up"
    DOWN = "down"
    TIMEOUT = "timeout"
    UNREACHABLE = "unreachable"
    WARN = "warn"

@dataclass(slots=True)
class ServiceConfig:
    id: str
    name: str
    container_name: Optional[str]
    url: Optional[str]
    group: str
    is_docker: bool

@dataclass(slots=True)
class DockerContainer:
    name: str
    id: str
    status: ContainerStatus = ContainerStatus.UNKNOWN


@dataclass(slots=True)
class ServiceState:
    service: ServiceConfig
    container_status: Optional[ContainerStatus]
    url_status: Optional[URLStatus]
    service_status: ServiceStatus = ServiceStatus.UNKNOWN
