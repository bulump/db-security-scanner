"""
CIS Benchmark Hard-Coded Rules
Provides precise validation for critical CIS PostgreSQL requirements.
"""
from typing import Dict, Any, List


class CISBenchmarkRules:
    """Hard-coded CIS Benchmark rules for PostgreSQL."""

    # CIS PostgreSQL 16 Benchmark v1.1

    @staticmethod
    def check_2_2_logging_collector(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        CIS 2.2: Ensure the logging collector is enabled

        Rationale: The logging_collector setting must be enabled to capture
        server log messages.
        """
        value = config.get('logging_collector', {}).get('value', 'off')

        return {
            'check_id': '2.2',
            'title': 'Ensure the logging collector is enabled',
            'requirement': 'logging_collector must be set to ON',
            'current_value': value,
            'required_value': 'on',
            'status': 'PASS' if value == 'on' else 'FAIL',
            'severity': 'high',
            'remediation': 'Set logging_collector = on in postgresql.conf'
        }

    @staticmethod
    def check_2_3_log_connections(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        CIS 2.3: Ensure log_connections is enabled

        Rationale: Enables logging of connection attempts to the server, which
        is useful for security auditing.
        """
        value = config.get('log_connections', {}).get('value', 'off')

        return {
            'check_id': '2.3',
            'title': 'Ensure log_connections is enabled',
            'requirement': 'log_connections must be set to ON',
            'current_value': value,
            'required_value': 'on',
            'status': 'PASS' if value == 'on' else 'FAIL',
            'severity': 'medium',
            'remediation': 'Set log_connections = on in postgresql.conf'
        }

    @staticmethod
    def check_2_4_log_disconnections(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        CIS 2.4: Ensure log_disconnections is enabled
        """
        value = config.get('log_disconnections', {}).get('value', 'off')

        return {
            'check_id': '2.4',
            'title': 'Ensure log_disconnections is enabled',
            'requirement': 'log_disconnections must be set to ON',
            'current_value': value,
            'required_value': 'on',
            'status': 'PASS' if value == 'on' else 'FAIL',
            'severity': 'medium',
            'remediation': 'Set log_disconnections = on in postgresql.conf'
        }

    @staticmethod
    def check_4_2_ssl_enabled(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        CIS 4.2: Ensure SSL is enabled

        Rationale: PostgreSQL should use SSL connections to encrypt network
        traffic between clients and server.
        """
        value = config.get('ssl', {}).get('value', 'off')

        return {
            'check_id': '4.2',
            'title': 'Ensure SSL is enabled',
            'requirement': 'ssl must be set to ON',
            'current_value': value,
            'required_value': 'on',
            'status': 'PASS' if value == 'on' else 'FAIL',
            'severity': 'critical',
            'remediation': 'Set ssl = on in postgresql.conf and configure SSL certificates'
        }

    @staticmethod
    def check_4_3_password_encryption(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        CIS 4.3: Ensure password_encryption is set to scram-sha-256

        Rationale: MD5 encryption is deprecated and weak. SCRAM-SHA-256
        provides stronger password hashing.
        """
        value = config.get('password_encryption', {}).get('value', 'md5')

        return {
            'check_id': '4.3',
            'title': 'Ensure password_encryption uses SCRAM-SHA-256',
            'requirement': 'password_encryption must be scram-sha-256',
            'current_value': value,
            'required_value': 'scram-sha-256',
            'status': 'PASS' if value == 'scram-sha-256' else 'FAIL',
            'severity': 'critical',
            'remediation': 'Set password_encryption = scram-sha-256 in postgresql.conf'
        }

    @staticmethod
    def check_2_5_log_statement(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        CIS 2.5: Ensure log_statement is set appropriately

        Rationale: At minimum, DDL (Data Definition Language) statements
        should be logged for audit purposes.
        """
        value = config.get('log_statement', {}).get('value', 'none')
        acceptable_values = ['ddl', 'mod', 'all']

        return {
            'check_id': '2.5',
            'title': 'Ensure log_statement is set to ddl or higher',
            'requirement': 'log_statement must be ddl, mod, or all',
            'current_value': value,
            'required_value': 'ddl (minimum)',
            'status': 'PASS' if value in acceptable_values else 'FAIL',
            'severity': 'high',
            'remediation': 'Set log_statement = ddl (or mod/all) in postgresql.conf'
        }

    @classmethod
    def run_all_checks(cls, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Run all CIS benchmark checks."""
        checks = [
            cls.check_2_2_logging_collector(config),
            cls.check_2_3_log_connections(config),
            cls.check_2_4_log_disconnections(config),
            cls.check_2_5_log_statement(config),
            cls.check_4_2_ssl_enabled(config),
            cls.check_4_3_password_encryption(config),
        ]

        return checks

    @classmethod
    def get_compliance_summary(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get summary of CIS compliance."""
        checks = cls.run_all_checks(config)

        total = len(checks)
        passed = sum(1 for c in checks if c['status'] == 'PASS')
        failed = total - passed

        critical_failures = [c for c in checks if c['status'] == 'FAIL' and c['severity'] == 'critical']

        return {
            'total_checks': total,
            'passed': passed,
            'failed': failed,
            'compliance_percentage': (passed / total * 100) if total > 0 else 0,
            'critical_failures': len(critical_failures),
            'all_checks': checks,
            'note': 'This is a subset of CIS checks. Full compliance requires 50+ checks.'
        }
