"""
Tests for CIS PostgreSQL 16 Benchmark compliance rules.
"""
import pytest
from src.agents.cis_rules import CISBenchmarkRules


class TestCISPostgreSQLRules:
    """Test suite for CIS PostgreSQL 16 Benchmark validation."""

    def test_check_2_2_logging_collector_enabled(self):
        """Test CIS 2.2 - logging_collector should be on (PASS)."""
        config = {'logging_collector': {'value': 'on'}}
        result = CISBenchmarkRules.run_all_checks(config)

        # Find check 2.2
        check_2_2 = next(c for c in result if c['check_id'] == '2.2')

        assert check_2_2['status'] == 'PASS'
        assert check_2_2['title'] == 'Ensure the logging collector is enabled'

    def test_check_2_2_logging_collector_disabled(self):
        """Test CIS 2.2 - logging_collector disabled should fail."""
        config = {'logging_collector': {'value': 'off'}}
        result = CISBenchmarkRules.run_all_checks(config)

        check_2_2 = next(c for c in result if c['check_id'] == '2.2')

        assert check_2_2['status'] == 'FAIL'
        assert check_2_2['severity'] == 'high'

    def test_check_2_3_log_connections_enabled(self):
        """Test CIS 2.3 - log_connections should be on (PASS)."""
        config = {'log_connections': {'value': 'on'}}
        result = CISBenchmarkRules.run_all_checks(config)

        check_2_3 = next(c for c in result if c['check_id'] == '2.3')

        assert check_2_3['status'] == 'PASS'
        assert check_2_3['title'] == 'Ensure log_connections is enabled'

    def test_check_2_3_log_connections_disabled(self):
        """Test CIS 2.3 - log_connections disabled should fail."""
        config = {'log_connections': {'value': 'off'}}
        result = CISBenchmarkRules.run_all_checks(config)

        check_2_3 = next(c for c in result if c['check_id'] == '2.3')

        assert check_2_3['status'] == 'FAIL'
        assert check_2_3['severity'] == 'medium'

    def test_check_2_4_log_disconnections_enabled(self):
        """Test CIS 2.4 - log_disconnections should be on (PASS)."""
        config = {'log_disconnections': {'value': 'on'}}
        result = CISBenchmarkRules.run_all_checks(config)

        check_2_4 = next(c for c in result if c['check_id'] == '2.4')

        assert check_2_4['status'] == 'PASS'

    def test_check_2_5_log_statement_ddl(self):
        """Test CIS 2.5 - log_statement should be ddl or higher."""
        # Test with ddl (PASS)
        config = {'log_statement': {'value': 'ddl'}}
        result = CISBenchmarkRules.run_all_checks(config)
        check_2_5 = next(c for c in result if c['check_id'] == '2.5')
        assert check_2_5['status'] == 'PASS'

        # Test with none (FAIL)
        config = {'log_statement': {'value': 'none'}}
        result = CISBenchmarkRules.run_all_checks(config)
        check_2_5 = next(c for c in result if c['check_id'] == '2.5')
        assert check_2_5['status'] == 'FAIL'

    def test_check_4_2_ssl_enabled(self):
        """Test CIS 4.2 - SSL should be enabled."""
        config = {'ssl': {'value': 'on'}}
        result = CISBenchmarkRules.run_all_checks(config)

        check_4_2 = next(c for c in result if c['check_id'] == '4.2')

        assert check_4_2['status'] == 'PASS'
        assert check_4_2['title'] == 'Ensure SSL is enabled'

    def test_check_4_2_ssl_disabled(self):
        """Test CIS 4.2 - SSL disabled should fail with critical severity."""
        config = {'ssl': {'value': 'off'}}
        result = CISBenchmarkRules.run_all_checks(config)

        check_4_2 = next(c for c in result if c['check_id'] == '4.2')

        assert check_4_2['status'] == 'FAIL'
        assert check_4_2['severity'] == 'critical'

    def test_check_4_3_password_encryption(self):
        """Test CIS 4.3 - Password encryption should use scram-sha-256."""
        # Test with scram-sha-256 (PASS)
        config = {'password_encryption': {'value': 'scram-sha-256'}}
        result = CISBenchmarkRules.run_all_checks(config)
        check_4_3 = next(c for c in result if c['check_id'] == '4.3')
        assert check_4_3['status'] == 'PASS'

        # Test with md5 (FAIL)
        config = {'password_encryption': {'value': 'md5'}}
        result = CISBenchmarkRules.run_all_checks(config)
        check_4_3 = next(c for c in result if c['check_id'] == '4.3')
        assert check_4_3['status'] == 'FAIL'
        assert check_4_3['severity'] == 'critical'

    def test_all_checks_return_required_fields(self):
        """Test that all CIS checks return required fields."""
        config = {'log_connections': {'value': 'on'}}
        result = CISBenchmarkRules.run_all_checks(config)

        required_fields = ['check_id', 'title', 'requirement', 'status',
                          'current_value', 'severity', 'remediation']

        for check in result:
            for field in required_fields:
                assert field in check, f"Check {check.get('check_id')} missing {field}"

    def test_returns_all_six_checks(self):
        """Test that all 6 hard-coded CIS checks are returned."""
        config = {}
        result = CISBenchmarkRules.run_all_checks(config)

        # Should return exactly 6 checks
        assert len(result) == 6

        # Check all expected check IDs are present
        check_ids = [c['check_id'] for c in result]
        expected_ids = ['2.2', '2.3', '2.4', '2.5', '4.2', '4.3']
        assert sorted(check_ids) == sorted(expected_ids)

    def test_missing_config_values_handled(self):
        """Test that missing configuration values are handled gracefully."""
        config = {}  # Empty config
        result = CISBenchmarkRules.run_all_checks(config)

        # Should still return 6 checks
        assert len(result) == 6

        # All should be FAIL
        for check in result:
            assert check['status'] == 'FAIL'

    def test_compliance_summary(self):
        """Test compliance summary calculation."""
        config = {
            'logging_collector': {'value': 'on'},
            'log_connections': {'value': 'on'},
            'log_disconnections': {'value': 'on'},
            'log_statement': {'value': 'ddl'},
            'ssl': {'value': 'on'},
            'password_encryption': {'value': 'scram-sha-256'}
        }

        summary = CISBenchmarkRules.get_compliance_summary(config)

        assert summary['total_checks'] == 6
        assert summary['passed'] == 6
        assert summary['failed'] == 0
        assert summary['compliance_percentage'] == 100.0
