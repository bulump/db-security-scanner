"""
Tests for the Flask web application endpoints.
"""
import pytest
from unittest.mock import Mock, patch
import json
from app import app


@pytest.fixture
def client():
    """Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestFlaskEndpoints:
    """Test suite for Flask application endpoints."""

    def test_index_route_loads(self, client):
        """Test that the home page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200

    def test_health_endpoint(self, client):
        """Test health check endpoint returns healthy status."""
        response = client.get('/health')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'healthy'

    @patch('app.DatabaseSecurityScanner')
    def test_scan_endpoint_success(self, mock_scanner, client, sample_scan_report):
        """Test successful scan execution."""
        # Setup mock
        mock_scanner_instance = Mock()
        mock_scanner_instance.scan.return_value = sample_scan_report
        mock_scanner.return_value = mock_scanner_instance

        # Make request
        response = client.post('/scan', json={
            'host': 'localhost',
            'port': 5432,
            'database': 'testdb',
            'user': 'postgres',
            'password': 'password',
            'compliance_framework': 'CIS'
        })

        # Assertions
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'scan_id' in data
        assert 'summary' in data
        assert data['summary']['database'] == 'testdb'

    def test_scan_endpoint_missing_required_fields(self, client):
        """Test scan endpoint with missing required fields."""
        response = client.post('/scan', json={
            'host': 'localhost',
            'port': 5432
            # Missing database and user
        })

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    @patch('app.DatabaseSecurityScanner')
    def test_scan_endpoint_scanner_error(self, mock_scanner, client):
        """Test scan endpoint handles scanner errors gracefully."""
        # Setup mock to raise exception
        mock_scanner_instance = Mock()
        mock_scanner_instance.scan.side_effect = Exception("Database connection failed")
        mock_scanner.return_value = mock_scanner_instance

        response = client.post('/scan', json={
            'host': 'localhost',
            'port': 5432,
            'database': 'testdb',
            'user': 'postgres',
            'password': 'password'
        })

        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data

    def test_results_endpoint_not_found(self, client):
        """Test results endpoint with non-existent scan ID."""
        response = client.get('/results/nonexistent_scan_id')
        assert response.status_code == 404

    def test_api_results_json_not_found(self, client):
        """Test JSON API endpoint with non-existent scan ID."""
        response = client.get('/api/results/nonexistent_scan_id')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_api_results_pdf_not_found(self, client):
        """Test PDF API endpoint with non-existent scan ID."""
        response = client.get('/api/results/nonexistent_scan_id/pdf')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    @patch('app.scan_results')
    def test_api_results_json_success(self, mock_results, client, sample_scan_report):
        """Test successful JSON results retrieval."""
        # Setup mock
        scan_id = 'test_scan_123'
        mock_results.get.return_value = sample_scan_report

        response = client.get(f'/api/results/{scan_id}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['security_score'] == 75

    @patch('app.scan_results')
    @patch('app.ReportGenerator')
    def test_api_results_pdf_success(self, mock_generator, mock_results, client, sample_scan_report):
        """Test successful PDF generation and download."""
        # Setup mocks
        scan_id = 'test_scan_123'
        mock_results.get.return_value = sample_scan_report
        mock_generator.generate_pdf.return_value = b'%PDF-1.4 fake pdf content'

        response = client.get(f'/api/results/{scan_id}/pdf')

        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
        assert response.headers.get('Content-Disposition', '').startswith('attachment')
