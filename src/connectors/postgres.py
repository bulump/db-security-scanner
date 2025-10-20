"""
PostgreSQL database connector.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Any
from .base import DatabaseConnector


class PostgreSQLConnector(DatabaseConnector):
    """PostgreSQL database connector implementation."""

    def connect(self) -> bool:
        """Establish PostgreSQL connection."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor
            )
            return True
        except psycopg2.Error as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self) -> None:
        """Close PostgreSQL connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def _execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a query and return results."""
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_version(self) -> str:
        """Get PostgreSQL version."""
        result = self._execute_query("SELECT version();")
        return result[0]['version'] if result else "Unknown"

    def get_configuration(self) -> Dict[str, Any]:
        """Get all configuration parameters."""
        query = """
            SELECT name, setting, unit, category, short_desc
            FROM pg_settings
            ORDER BY category, name;
        """
        results = self._execute_query(query)
        return {row['name']: {
            'value': row['setting'],
            'unit': row['unit'],
            'category': row['category'],
            'description': row['short_desc']
        } for row in results}

    def get_users(self) -> List[Dict[str, Any]]:
        """Get database users and roles."""
        query = """
            SELECT
                rolname as username,
                rolsuper as is_superuser,
                rolcreaterole as can_create_role,
                rolcreatedb as can_create_db,
                rolcanlogin as can_login,
                rolreplication as is_replication,
                rolbypassrls as bypass_rls,
                rolvaliduntil as valid_until
            FROM pg_roles
            ORDER BY rolname;
        """
        return self._execute_query(query)

    def get_security_settings(self) -> Dict[str, Any]:
        """Get security-related configuration."""
        security_params = [
            'ssl', 'ssl_cert_file', 'ssl_key_file', 'ssl_ca_file',
            'password_encryption', 'ssl_min_protocol_version',
            'log_connections', 'log_disconnections',
            'log_statement', 'logging_collector',
            'max_connections', 'superuser_reserved_connections',
            'authentication_timeout', 'tcp_keepalives_idle'
        ]

        config = self.get_configuration()
        return {
            param: config.get(param, {'value': 'Not Set'})
            for param in security_params
        }

    def check_encryption(self) -> Dict[str, bool]:
        """Check encryption status."""
        config = self.get_configuration()

        ssl_enabled = config.get('ssl', {}).get('value') == 'on'

        # Check if data directory encryption is enabled (pg_crypto)
        query = "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'pgcrypto');"
        result = self._execute_query(query)
        pgcrypto_installed = result[0]['exists'] if result else False

        return {
            'ssl_enabled': ssl_enabled,
            'encryption_extension_available': pgcrypto_installed,
            'password_encryption_enabled': config.get('password_encryption', {}).get('value') != 'md5'
        }

    def get_authentication_methods(self) -> List[str]:
        """Get configured authentication methods from pg_hba.conf (if accessible)."""
        # Note: This requires superuser privileges
        try:
            query = """
                SELECT type, database, user_name, address, auth_method
                FROM pg_hba_file_rules
                ORDER BY line_number;
            """
            return self._execute_query(query)
        except psycopg2.Error:
            return []

    def check_audit_logging(self) -> Dict[str, Any]:
        """Check if audit logging is properly configured."""
        config = self.get_configuration()

        return {
            'logging_collector': config.get('logging_collector', {}).get('value') == 'on',
            'log_connections': config.get('log_connections', {}).get('value') == 'on',
            'log_disconnections': config.get('log_disconnections', {}).get('value') == 'on',
            'log_statement': config.get('log_statement', {}).get('value'),
            'log_duration': config.get('log_duration', {}).get('value') == 'on',
        }
