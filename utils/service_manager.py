"""Service configuration and management module."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ServiceConfig:
    """Configuration for a single service."""

    service_id: str
    display_name: str
    base_url: str
    enabled: bool
    auth_config: Optional[Dict[str, Any]] = None
    apis: Optional[Dict[str, Any]] = None
    token_routing: Optional[Dict[str, str]] = None


class ServiceManager:
    """Centralized service configuration management."""

    def __init__(self, services_config: Dict[str, Any]):
        """Initialize ServiceManager with service configurations.

        Args:
            services_config: Dictionary with service IDs as keys and service configs as values
        """
        self.services: Dict[str, ServiceConfig] = {}
        self._load_services(services_config)

    def _load_services(self, config: Dict[str, Any]) -> None:
        """Load service configurations from dictionary.

        Args:
            config: Dictionary containing service configurations
        """
        for service_id, service_data in config.items():
            self.services[service_id] = ServiceConfig(
                service_id=service_id,
                display_name=service_data.get("display_name", service_id),
                base_url=service_data.get("base_url"),
                enabled=service_data.get("enabled", True),
                auth_config=service_data.get("auth"),
                apis=service_data.get("apis", {}),
                token_routing=service_data.get("token_routing", {}),
            )

    def get_enabled_services(self) -> List[ServiceConfig]:
        """Return list of enabled services.

        Returns:
            List of ServiceConfig objects with enabled=True
        """
        return [s for s in self.services.values() if s.enabled]

    def get_service(self, service_id: str) -> Optional[ServiceConfig]:
        """Get service configuration by ID.

        Args:
            service_id: The service identifier

        Returns:
            ServiceConfig if found, None otherwise
        """
        return self.services.get(service_id)

    def get_service_base_url(self, service_id: str) -> str:
        """Get base URL for a service.

        Args:
            service_id: The service identifier

        Returns:
            Base URL string, empty string if service not found
        """
        service = self.get_service(service_id)
        return service.base_url if service else ""

    def get_service_apis(self, service_id: str) -> Dict[str, Any]:
        """Get API definitions for a service.

        Args:
            service_id: The service identifier

        Returns:
            Dictionary of API definitions
        """
        service = self.get_service(service_id)
        return service.apis if service else {}

    def get_service_auth_config(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get authentication configuration for a service.

        Args:
            service_id: The service identifier

        Returns:
            Auth config dictionary or None
        """
        service = self.get_service(service_id)
        return service.auth_config if service else None

    def get_service_token_routing(self, service_id: str) -> Dict[str, str]:
        """Get token routing configuration for a service.

        Args:
            service_id: The service identifier

        Returns:
            Token routing dictionary
        """
        service = self.get_service(service_id)
        return service.token_routing if service else {}

    def is_service_enabled(self, service_id: str) -> bool:
        """Check if a service is enabled.

        Args:
            service_id: The service identifier

        Returns:
            True if enabled, False otherwise
        """
        service = self.get_service(service_id)
        return service.enabled if service else False

    def enable_service(self, service_id: str) -> None:
        """Enable a service.

        Args:
            service_id: The service identifier
        """
        if service_id in self.services:
            self.services[service_id].enabled = True

    def disable_service(self, service_id: str) -> None:
        """Disable a service.

        Args:
            service_id: The service identifier
        """
        if service_id in self.services:
            self.services[service_id].enabled = False

    def apply_env_filter(
        self, enabled_services: Optional[List[str]] = None, disabled_services: Optional[List[str]] = None
    ) -> None:
        """Apply environment-based service filtering.

        Args:
            enabled_services: List of services to enable. If provided, only these are enabled.
            disabled_services: List of services to disable.
        """
        if enabled_services:
            for service_id in self.services:
                self.services[service_id].enabled = service_id in enabled_services

        if disabled_services:
            for service_id in disabled_services:
                if service_id in self.services:
                    self.services[service_id].enabled = False

    def get_all_services(self) -> Dict[str, ServiceConfig]:
        """Get all services (enabled and disabled).

        Returns:
            Dictionary of all services
        """
        return self.services

    def get_services_by_status(self, enabled_only: bool = True) -> List[str]:
        """Get list of service IDs filtered by enabled status.

        Args:
            enabled_only: If True, return only enabled services

        Returns:
            List of service IDs
        """
        if enabled_only:
            return [sid for sid, svc in self.services.items() if svc.enabled]
        return list(self.services.keys())
