"""
Main Database Security Scanner
Orchestrates all agents to perform comprehensive security analysis.
"""
from typing import Dict, Any
from .connectors import PostgreSQLConnector
from .agents import ConfigAnalyzerAgent, VulnerabilityDetectorAgent, ComplianceCheckerAgent


class DatabaseSecurityScanner:
    """Main scanner that coordinates all security analysis agents."""

    def __init__(self, api_key: str = None):
        """Initialize scanner with AI agents."""
        self.config_analyzer = ConfigAnalyzerAgent(api_key)
        self.vulnerability_detector = VulnerabilityDetectorAgent(api_key)
        self.compliance_checker = ComplianceCheckerAgent(api_key)

    def scan(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        compliance_framework: str = "CIS"
    ) -> Dict[str, Any]:
        """
        Perform comprehensive security scan of database.

        Args:
            host: Database host
            port: Database port
            database: Database name
            user: Username
            password: Password
            compliance_framework: Framework to check against (CIS, STIG, etc.)

        Returns:
            Complete security analysis report
        """
        print(f"🔍 Starting security scan of {database} on {host}:{port}")

        # Connect to database and gather information
        print("📊 Gathering database information...")
        with PostgreSQLConnector(host, port, database, user, password) as db:
            db_info = {
                'version': db.get_version(),
                'configuration': db.get_configuration(),
                'users': db.get_users(),
                'security_settings': db.get_security_settings(),
                'encryption': db.check_encryption(),
                'audit_logging': db.check_audit_logging()
            }

        print(f"✓ Connected to PostgreSQL: {db_info['version'][:50]}...")

        # Run AI agents in parallel (or sequentially for now)
        print("\n🤖 Running AI Security Analysis...")

        print("  → Configuration Analysis...")
        config_analysis = self.config_analyzer.analyze(
            db_info['configuration'],
            db_type="postgresql"
        )

        print("  → Vulnerability Detection...")
        vulnerability_analysis = self.vulnerability_detector.detect(db_info)

        print("  → Compliance Checking...")
        compliance_analysis = self.compliance_checker.check_compliance(
            db_info['configuration'],
            framework=compliance_framework,
            db_type="postgresql"
        )

        # Compile complete report
        report = {
            'scan_info': {
                'database': database,
                'host': host,
                'port': port,
                'version': db_info['version'],
                'compliance_framework': compliance_framework
            },
            'database_info': {
                'user_count': len(db_info['users']),
                'superuser_count': sum(1 for u in db_info['users'] if u.get('is_superuser')),
                'encryption_status': db_info['encryption'],
                'audit_logging_status': db_info['audit_logging']
            },
            'configuration_analysis': config_analysis,
            'vulnerability_analysis': vulnerability_analysis,
            'compliance_analysis': compliance_analysis,
            'overall_risk_assessment': self._calculate_overall_risk(
                config_analysis,
                vulnerability_analysis,
                compliance_analysis
            )
        }

        print("\n✅ Scan complete!")
        return report

    def _calculate_overall_risk(
        self,
        config_analysis: Dict[str, Any],
        vuln_analysis: Dict[str, Any],
        compliance_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate overall risk score and level."""
        # Simple risk calculation
        risk_score = 100  # Start with perfect score

        # Deduct points for issues
        critical_issues = len(config_analysis.get('critical_issues', []))
        warnings = len(config_analysis.get('warnings', []))
        vulnerabilities = len(vuln_analysis.get('vulnerabilities', []))
        compliance_pct = compliance_analysis.get('compliance_percentage', 100)

        risk_score -= (critical_issues * 20)
        risk_score -= (warnings * 5)
        risk_score -= (vulnerabilities * 10)
        risk_score = min(risk_score, compliance_pct)
        risk_score = max(0, risk_score)

        if risk_score >= 90:
            risk_level = "low"
        elif risk_score >= 70:
            risk_level = "medium"
        elif risk_score >= 50:
            risk_level = "high"
        else:
            risk_level = "critical"

        return {
            'security_score': risk_score,
            'risk_level': risk_level,
            'critical_issue_count': critical_issues,
            'warning_count': warnings,
            'vulnerability_count': vulnerabilities,
            'compliance_percentage': compliance_pct
        }
