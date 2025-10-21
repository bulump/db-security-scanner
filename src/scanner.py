"""
Main Database Security Scanner
Orchestrates all agents to perform comprehensive security analysis.
"""
from typing import Dict, Any
from .connectors import PostgreSQLConnector
from .agents import ConfigAnalyzerAgent, VulnerabilityDetectorAgent, ComplianceCheckerAgent
from .agents.cis_rules import CISBenchmarkRules


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
        config_analysis_raw = self.config_analyzer.analyze(
            db_info['configuration'],
            db_type="postgresql"
        )
        config_analysis = self._transform_config_analysis(config_analysis_raw)

        print("  → Vulnerability Detection...")
        vulnerability_analysis_raw = self.vulnerability_detector.detect(db_info)
        vulnerability_analysis = self._transform_vulnerability_analysis(vulnerability_analysis_raw)

        print("  → Compliance Checking...")
        # Use hard-coded CIS rules for PostgreSQL CIS framework
        db_type = "postgresql"
        if compliance_framework == "CIS" and db_type == "postgresql":
            compliance_checks = CISBenchmarkRules.run_all_checks(db_info['configuration'])
            compliance_analysis = self._transform_cis_checks(compliance_checks)
        else:
            # Use AI-based compliance checking for other frameworks
            compliance_analysis_raw = self.compliance_checker.check_compliance(
                db_info['configuration'],
                framework=compliance_framework,
                db_type="postgresql"
            )
            compliance_analysis = self._transform_compliance_analysis(compliance_analysis_raw)

        # Calculate overall risk assessment
        risk_assessment = self._calculate_overall_risk(
            config_analysis,
            vulnerability_analysis,
            compliance_analysis
        )

        # Compile complete report
        from datetime import datetime

        report = {
            'scan_info': {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'compliance_framework': compliance_framework
            },
            'database_info': {
                'database': database,
                'host': host,
                'port': port,
                'version': db_info['version'],
                'user_count': len(db_info['users']),
                'superuser_count': sum(1 for u in db_info['users'] if u.get('is_superuser')),
                'encryption_status': db_info['encryption'],
                'audit_logging_status': db_info['audit_logging']
            },
            'config_analysis': config_analysis,
            'vulnerability_analysis': vulnerability_analysis,
            'compliance_analysis': compliance_analysis,
            'security_score': risk_assessment['security_score'],
            'risk_level': risk_assessment['risk_level'].upper(),
            'critical_issues': risk_assessment['critical_issue_count'],
            'overall_risk_assessment': risk_assessment
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
        issues = config_analysis.get('issues', [])
        critical_issues = sum(1 for i in issues if i.get('severity') == 'critical')
        warnings = sum(1 for i in issues if i.get('severity') in ['medium', 'high'])
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

    def _transform_config_analysis(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Transform config analysis to template format."""
        issues = []

        # Add critical issues
        for item in raw.get('critical_issues', []):
            issues.append({
                'title': f"{item.get('parameter', 'Unknown')} Misconfiguration",
                'description': item.get('issue', ''),
                'severity': 'critical',
                'remediation': item.get('recommendation', '')
            })

        # Add warnings
        for item in raw.get('warnings', []):
            issues.append({
                'title': f"{item.get('parameter', 'Unknown')} Warning",
                'description': item.get('concern', ''),
                'severity': 'medium',
                'remediation': item.get('recommendation', '')
            })

        return {'issues': issues}

    def _transform_vulnerability_analysis(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Transform vulnerability analysis to template format."""
        vulnerabilities = []

        for item in raw.get('vulnerabilities', []):
            vulnerabilities.append({
                'title': item.get('title', 'Unknown Vulnerability'),
                'description': item.get('description', ''),
                'severity': item.get('severity', 'medium'),
                'cve_id': item.get('cve_id'),
                'remediation': item.get('remediation', '')
            })

        return {'vulnerabilities': vulnerabilities}

    def _transform_cis_checks(self, checks: list) -> Dict[str, Any]:
        """Transform hard-coded CIS checks to template format."""
        failed_checks = []
        passed_checks = 0
        total_checks = len(checks)

        for check in checks:
            if check.get('status') == 'PASS':
                passed_checks += 1
            else:
                failed_checks.append({
                    'check_id': check.get('check_id', 'Unknown'),
                    'title': check.get('title', ''),
                    'requirement': check.get('requirement', ''),
                    'current_value': check.get('current_value', ''),
                    'severity': check.get('severity', 'medium'),
                    'remediation': check.get('remediation', '')
                })

        compliance_percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 100

        return {
            'passed_checks': passed_checks,
            'total_checks': total_checks,
            'compliance_percentage': compliance_percentage,
            'failed_checks': failed_checks
        }

    def _transform_compliance_analysis(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Transform AI-based compliance analysis to template format."""
        # Handle AI response format with passed_checks and failed_checks arrays
        passed = raw.get('passed_checks', [])
        failed = raw.get('failed_checks', [])

        failed_checks = []
        for check in failed:
            failed_checks.append({
                'check_id': check.get('check_id', 'Unknown'),
                'title': check.get('title', ''),
                'requirement': check.get('requirement', ''),
                'current_value': check.get('current_state', ''),
                'severity': check.get('risk_level', 'medium'),
                'remediation': check.get('remediation', '')
            })

        total_checks = len(passed) + len(failed)
        passed_checks = len(passed)
        compliance_percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 100

        return {
            'passed_checks': passed_checks,
            'total_checks': total_checks,
            'compliance_percentage': compliance_percentage,
            'failed_checks': failed_checks
        }
