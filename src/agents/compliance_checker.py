"""
Compliance Checker Agent
Validates database configuration against compliance frameworks.
"""
import anthropic
import os
from typing import Dict, Any


class ComplianceCheckerAgent:
    """AI agent that checks database compliance against frameworks like CIS, STIG."""

    def __init__(self, api_key: str = None):
        """Initialize the agent with Anthropic API key."""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def check_compliance(
        self,
        config: Dict[str, Any],
        framework: str = "CIS",
        db_type: str = "postgresql"
    ) -> Dict[str, Any]:
        """
        Check compliance against specified framework.

        Args:
            config: Database configuration
            framework: Compliance framework (CIS, STIG, SOC2, HIPAA, PCI-DSS)
            db_type: Database type

        Returns:
            Compliance report
        """
        prompt = f"""You are a database compliance expert specializing in {framework} benchmarks.

Evaluate this {db_type.upper()} database against {framework} requirements.

CONFIGURATION SAMPLE:
{self._sample_config(config)}

Provide a compliance assessment with:
1. Overall compliance percentage
2. Passed checks
3. Failed checks with remediation steps
4. Recommendations for full compliance

Return JSON:
{{
    "framework": "{framework}",
    "compliance_percentage": 0-100,
    "overall_status": "compliant|non-compliant|partially_compliant",
    "passed_checks": [
        {{
            "check_id": "1.1",
            "title": "check title",
            "requirement": "requirement description"
        }}
    ],
    "failed_checks": [
        {{
            "check_id": "1.2",
            "title": "check title",
            "requirement": "requirement description",
            "current_state": "what's configured",
            "required_state": "what's required",
            "risk_level": "critical|high|medium|low",
            "remediation": "how to fix"
        }}
    ],
    "recommendations": [
        "recommendation 1",
        "recommendation 2"
    ]
}}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            import json
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            return json.loads(response_text)

        except Exception as e:
            return {
                "error": str(e),
                "framework": framework,
                "compliance_percentage": 0,
                "overall_status": "error",
                "passed_checks": [],
                "failed_checks": [],
                "recommendations": []
            }

    def _sample_config(self, config: Dict[str, Any], max_items: int = 30) -> str:
        """Sample configuration for compliance check."""
        lines = []
        for i, (key, value) in enumerate(config.items()):
            if i >= max_items:
                break
            if isinstance(value, dict):
                lines.append(f"  {key}: {value.get('value', str(value))}")
            else:
                lines.append(f"  {key}: {value}")
        return "\n".join(lines)
