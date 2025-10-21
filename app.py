"""
Flask Web Interface for Database Security Scanner
Provides a user-friendly web UI for running security scans and viewing results.
"""
from flask import Flask, render_template, request, jsonify, session
from src.scanner import DatabaseSecurityScanner
from src.reports.generator import ReportGenerator
import os
import json
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))

# Store scan results in memory (in production, use a database)
scan_results = {}


@app.route('/')
def index():
    """Home page with scan form."""
    return render_template('index.html')


@app.route('/scan', methods=['POST'])
def run_scan():
    """Run a security scan on the provided database."""
    try:
        # Get form data
        data = request.get_json()

        host = data.get('host', 'localhost')
        port = int(data.get('port', 5432))
        database = data.get('database')
        user = data.get('user')
        password = data.get('password', '')
        compliance_framework = data.get('compliance_framework', 'CIS')

        # Validate required fields
        if not all([database, user]):
            return jsonify({'error': 'Database name and user are required'}), 400

        # Initialize scanner
        scanner = DatabaseSecurityScanner()

        # Run scan
        report = scanner.scan(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            compliance_framework=compliance_framework
        )

        # Generate scan ID
        scan_id = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Store results
        scan_results[scan_id] = report

        # Generate reports
        markdown_report = ReportGenerator.generate_markdown(report)
        html_report = ReportGenerator.generate_html(report)
        json_report = json.dumps(report, indent=2)

        return jsonify({
            'success': True,
            'scan_id': scan_id,
            'summary': {
                'database': report['database_info']['database'],
                'security_score': report.get('security_score', 0),
                'risk_level': report.get('risk_level', 'UNKNOWN'),
                'critical_issues': report.get('critical_issues', 0),
                'scan_time': report['scan_info']['timestamp']
            },
            'report': report
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


@app.route('/results/<scan_id>')
def view_results(scan_id):
    """View scan results."""
    report = scan_results.get(scan_id)

    if not report:
        return "Scan not found", 404

    return render_template('results.html', report=report, scan_id=scan_id)


@app.route('/api/results/<scan_id>')
def get_results_json(scan_id):
    """Get scan results as JSON."""
    report = scan_results.get(scan_id)

    if not report:
        return jsonify({'error': 'Scan not found'}), 404

    return jsonify(report)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    # Run the app
    port = int(os.getenv('FLASK_PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
