from pathlib import Path
import yaml
from app.models import ServiceConfig

class ServiceRegistry:

    def __init__(self):
        self.services: dict[str, ServiceConfig] = {}

    def load_config(self, config_path: Path = Path("config.yaml")) -> None:

        if not config_path.exists():
            self.services.clear()
            return

        with config_path.open("r", encoding='utf-8') as config:
            raw = yaml.safe_load(config) or {}

        services_list = raw.get("services", []) or []
        self.services.clear()

        for item in services_list:
            container_name = item.get("container_name")
            svc = ServiceConfig(
                id=item["id"],
                name=item["name"],
                container_name=container_name,
                url=item.get("url"),
                group=item.get("group", "default"),
                is_docker=bool(container_name),
            )
            self.services[svc.id] = svc


registry = ServiceRegistry()
registry.load_config()  # Load on import
SERVICE_DEFS = registry.services
