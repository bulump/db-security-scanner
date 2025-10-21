"""
Tests for the report generator module.
"""
import pytest
import json
from src.reports.generator import ReportGenerator


class TestReportGenerator:
    """Test suite for report generation in various formats."""

    def test_generate_markdown(self, sample_scan_report):
        """Test markdown report generation produces valid output."""
        result = ReportGenerator.generate_markdown(sample_scan_report)

        # Check it's a string
        assert isinstance(result, str)

        # Check for key sections
        assert "Database Security Scan Report" in result
        assert "testdb" in result
        assert "75" in result  # Security score
        assert "medium" in result.lower()  # Risk level

        # Check for configuration analysis section
        assert "Configuration Analysis" in result

        # Check for compliance section
        assert "CIS" in result

    def test_generate_json(self, sample_scan_report):
        """Test JSON report generation produces valid JSON."""
        result = ReportGenerator.generate_json(sample_scan_report)

        # Check it's a string
        assert isinstance(result, str)

        # Parse and validate JSON
        parsed = json.loads(result)
        assert parsed['security_score'] == 75
        assert parsed['risk_level'] == 'medium'
        assert parsed['database_info']['database'] == 'testdb'
        assert parsed['database_info']['host'] == 'localhost'
        assert parsed['database_info']['port'] == 5432

    def test_generate_pdf(self, sample_scan_report):
        """Test PDF report generation produces valid PDF bytes."""
        result = ReportGenerator.generate_pdf(sample_scan_report)

        # Check it's bytes
        assert isinstance(result, bytes)

        # Check PDF header (all PDFs start with %PDF)
        assert result.startswith(b'%PDF')

        # Check it's substantial (more than just empty PDF)
        assert len(result) > 1000

        # Check PDF footer
        assert b'%%EOF' in result

    def test_generate_html(self, sample_scan_report):
        """Test HTML report generation produces valid HTML."""
        result = ReportGenerator.generate_html(sample_scan_report)

        # Check it's a string
        assert isinstance(result, str)

        # Check for HTML structure
        assert "<!DOCTYPE html>" in result
        assert "<html>" in result
        assert "</html>" in result

        # Check for content
        assert "Database Security Scan Report" in result
        assert "testdb" in result

    def test_markdown_includes_vulnerabilities(self, sample_scan_report):
        """Test markdown report includes vulnerability details."""
        result = ReportGenerator.generate_markdown(sample_scan_report)

        assert "Vulnerability Analysis" in result
        assert "Weak Password Encryption" in result

    def test_markdown_includes_compliance(self, sample_scan_report):
        """Test markdown report includes compliance details."""
        result = ReportGenerator.generate_markdown(sample_scan_report)

        assert "Compliance" in result
        assert "66.7%" in result or "67" in result

    def test_pdf_handles_long_version_string(self, sample_scan_report):
        """Test PDF generation handles long version strings without overflow."""
        # Create a report with a very long version string
        long_version_report = sample_scan_report.copy()
        long_version_report['database_info'] = sample_scan_report['database_info'].copy()
        long_version_report['database_info']['version'] = (
            'PostgreSQL 16.1 on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) '
            '12.2.0, 64-bit with additional very long configuration details that might '
            'cause overflow issues if word wrapping is not properly implemented in the report'
        )

        result = ReportGenerator.generate_pdf(long_version_report)

        # Should still generate valid PDF
        assert isinstance(result, bytes)
        assert result.startswith(b'%PDF')
        assert len(result) > 1000  # Valid PDF with content

    def test_json_report_is_properly_indented(self, sample_scan_report):
        """Test JSON report uses proper indentation."""
        result = ReportGenerator.generate_json(sample_scan_report)

        # Check for indentation (indent=2 in implementation)
        lines = result.split('\n')
        assert len(lines) > 10  # Should be multi-line
        assert any('  ' in line for line in lines)  # Should have indentation
