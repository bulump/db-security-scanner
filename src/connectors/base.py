"""
Base database connector interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any


class DatabaseConnector(ABC):
    """Abstract base class for database connectors."""

    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    @abstractmethod
    def connect(self) -> bool:
        """Establish database connection."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection."""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Get database version."""
        pass

    @abstractmethod
    def get_configuration(self) -> Dict[str, Any]:
        """Get database configuration parameters."""
        pass

    @abstractmethod
    def get_users(self) -> List[Dict[str, Any]]:
        """Get list of database users and their privileges."""
        pass

    @abstractmethod
    def get_security_settings(self) -> Dict[str, Any]:
        """Get security-related settings."""
        pass

    @abstractmethod
    def check_encryption(self) -> Dict[str, bool]:
        """Check encryption status (at rest, in transit)."""
        pass

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
