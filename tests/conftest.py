"""
Shared test fixtures for the database security scanner test suite.
"""
import pytest
from datetime import datetime


@pytest.fixture
def sample_db_info():
    """Sample database information for testing."""
    return {
        'version': 'PostgreSQL 16.1 on x86_64-pc-linux-gnu, compiled by gcc',
        'database': 'testdb',
        'host': 'localhost',
        'port': 5432,
        'users': [
            {'username': 'admin', 'is_superuser': True},
            {'username': 'app_user', 'is_superuser': False}
        ],
        'security_settings': {
            'ssl': {'value': 'on'},
            'password_encryption': {'value': 'scram-sha-256'},
            'log_connections': {'value': 'on'},
            'log_disconnections': {'value': 'on'}
        },
        'encryption': {
            'ssl_enabled': True,
            'data_encryption': False
        }
    }


@pytest.fixture
def sample_config():
    """Sample PostgreSQL configuration for CIS testing."""
    return {
        'log_connections': {'value': 'on'},
        'log_disconnections': {'value': 'on'},
        'log_error_verbosity': {'value': 'default'},
        'log_hostname': {'value': 'off'},
        'log_line_prefix': {'value': '%m [%p] %q%u@%d '},
        'log_statement': {'value': 'ddl'},
        'ssl': {'value': 'on'},
        'password_encryption': {'value': 'scram-sha-256'}
    }


@pytest.fixture
def sample_scan_report():
    """Sample complete scan report."""
    return {
        'scan_info': {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'compliance_framework': 'CIS',
            'scanner_version': '1.0.0'
        },
        'database_info': {
            'database': 'testdb',
            'host': 'localhost',
            'port': 5432,
            'version': 'PostgreSQL 16.1 on x86_64-pc-linux-gnu'
        },
        'security_score': 75,
        'risk_level': 'medium',
        'critical_issues': 2,
        'config_analysis': {
            'issues': [
                {
                    'severity': 'critical',
                    'title': 'SSL Not Enforced',
                    'description': 'Database allows unencrypted connections',
                    'remediation': 'Set ssl=on in postgresql.conf'
                }
            ]
        },
        'vulnerability_analysis': {
            'vulnerabilities': [
                {
                    'severity': 'high',
                    'title': 'Weak Password Encryption',
                    'description': 'Using MD5 password encryption',
                    'cve_id': None,
                    'remediation': 'Update to scram-sha-256'
                }
            ]
        },
        'compliance_analysis': {
            'total_checks': 6,
            'passed_checks': 4,
            'failed_checks': [
                {
                    'check_id': '2.2',
                    'title': 'Ensure logging of connections is enabled',
                    'requirement': 'log_connections should be on',
                    'current_value': 'off',
                    'severity': 'high',
                    'remediation': 'Set log_connections = on in postgresql.conf'
                }
            ],
            'compliance_percentage': 66.7
        },
        'overall_risk_assessment': {
            'security_score': 75,
            'risk_level': 'medium',
            'critical_issue_count': 2,
            'warning_count': 3,
            'vulnerability_count': 1,
            'compliance_percentage': 66.7
        }
    }
