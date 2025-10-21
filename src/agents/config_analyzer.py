"""
Configuration Analyzer Agent
Analyzes database configuration for security issues.
"""
import anthropic
import os
from typing import Dict, Any, List


class ConfigAnalyzerAgent:
    """AI agent that analyzes database configurations for security issues."""

    def __init__(self, api_key: str = None):
        """Initialize the agent with Anthropic API key."""
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def analyze(self, config: Dict[str, Any], db_type: str = "postgresql") -> Dict[str, Any]:
        """
        Analyze database configuration and identify security issues.

        Args:
            config: Dictionary of configuration parameters
            db_type: Type of database (postgresql)

        Returns:
            Dictionary containing analysis results and recommendations
        """
        # Prepare configuration data for analysis
        config_summary = self._prepare_config_summary(config)

        prompt = f"""You are an expert database security analyst with 20+ years of experience.
Analyze this {db_type.upper()} database configuration and identify security issues, misconfigurations, and provide recommendations.

DATABASE CONFIGURATION:
{config_summary}

Please provide a comprehensive security analysis including:

1. CRITICAL ISSUES: Configuration settings that pose immediate security risks
2. WARNINGS: Settings that should be improved for better security
3. BEST PRACTICES: Recommendations for optimal security posture
4. COMPLIANCE CONCERNS: Settings that may affect CIS/STIG compliance

Format your response as JSON with the following structure:
{{
    "overall_risk_level": "critical|high|medium|low",
    "critical_issues": [
        {{
            "parameter": "parameter_name",
            "current_value": "value",
            "issue": "description of the security issue",
            "recommendation": "specific remediation steps",
            "cve_references": ["CVE-XXXX-XXXX"] // if applicable
        }}
    ],
    "warnings": [
        {{
            "parameter": "parameter_name",
            "current_value": "value",
            "concern": "description",
            "recommendation": "improvement steps"
        }}
    ],
    "best_practices": [
        {{
            "area": "category",
            "recommendation": "specific recommendation",
            "benefit": "security benefit description"
        }}
    ],
    "compliance_notes": [
        {{
            "framework": "CIS|STIG|SOC2|etc",
            "requirement": "requirement description",
            "status": "compliant|non-compliant|needs_review",
            "remediation": "steps if non-compliant"
        }}
    ]
}}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the response
            response_text = message.content[0].text

            # Parse JSON response
            import json
            # Find JSON in response (handle markdown code blocks if present)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            analysis = json.loads(response_text)
            return analysis

        except Exception as e:
            return {
                "error": str(e),
                "overall_risk_level": "unknown",
                "critical_issues": [],
                "warnings": [],
                "best_practices": [],
                "compliance_notes": []
            }

    def _prepare_config_summary(self, config: Dict[str, Any], max_params: int = 50) -> str:
        """Prepare a summary of configuration for AI analysis."""
        # Focus on security-relevant parameters
        security_keywords = [
            'ssl', 'password', 'auth', 'log', 'encrypt', 'security',
            'max_connections', 'timeout', 'trust', 'md5', 'scram'
        ]

        # Filter relevant parameters
        relevant_params = {}
        for param, details in config.items():
            if any(keyword in param.lower() for keyword in security_keywords):
                if isinstance(details, dict):
                    relevant_params[param] = details.get('value', str(details))
                else:
                    relevant_params[param] = str(details)

        # Format for readability
        summary_lines = []
        for param, value in list(relevant_params.items())[:max_params]:
            summary_lines.append(f"  {param}: {value}")

        return "\n".join(summary_lines)
