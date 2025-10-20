"""
Sample Database Security Scan
Demonstrates how to use the DB Security Scanner.
"""
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.scanner import DatabaseSecurityScanner
from src.reports.generator import ReportGenerator

# Load environment variables
load_dotenv()


def main():
    """Run a sample security scan."""
    print("=" * 70)
    print("AI-Powered Database Security Scanner")
    print("Combining 20+ years of expertise with modern AI")
    print("=" * 70)
    print()

    # Initialize scanner
    scanner = DatabaseSecurityScanner()

    # Scan parameters (update these for your database)
    scan_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME', 'postgres'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'compliance_framework': 'CIS'  # CIS, STIG, SOC2, HIPAA, PCI-DSS
    }

    try:
        # Perform scan
        report = scanner.scan(**scan_params)

        # Generate reports
        print("\n📄 Generating reports...")

        # Markdown report
        md_report = ReportGenerator.generate_markdown(report)
        with open('security_report.md', 'w') as f:
            f.write(md_report)
        print("  ✓ Markdown report saved to: security_report.md")

        # JSON report
        json_report = ReportGenerator.generate_json(report)
        with open('security_report.json', 'w') as f:
            f.write(json_report)
        print("  ✓ JSON report saved to: security_report.json")

        # HTML report
        html_report = ReportGenerator.generate_html(report)
        with open('security_report.html', 'w') as f:
            f.write(html_report)
        print("  ✓ HTML report saved to: security_report.html")

        # Print summary
        risk = report['overall_risk_assessment']
        print("\n" + "=" * 70)
        print("SCAN SUMMARY")
        print("=" * 70)
        print(f"Security Score: {risk['security_score']}/100")
        print(f"Risk Level: {risk['risk_level'].upper()}")
        print(f"Critical Issues: {risk['critical_issue_count']}")
        print(f"Vulnerabilities: {risk['vulnerability_count']}")
        print(f"Compliance: {risk['compliance_percentage']}%")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error during scan: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
