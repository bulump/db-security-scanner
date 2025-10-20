# 🔒 AI-Powered Database Security Scanner

An intelligent database security analysis tool that combines 20+ years of database security expertise with modern AI capabilities using Claude AI.

## 🎯 Project Overview

This project demonstrates the application of AI agents to database security - automating security audits, vulnerability detection, and compliance checking that traditionally required manual expert analysis.

**Key Innovation**: Leveraging Claude AI to encode deep domain expertise into autonomous agents that can analyze database configurations, detect vulnerabilities, and generate compliance reports at scale.

## ✨ Features

- **🤖 Multi-Agent AI System**: Three specialized AI agents working together
  - **Configuration Analyzer**: Identifies security misconfigurations
  - **Vulnerability Detector**: Finds known vulnerabilities and CVEs
  - **Compliance Checker**: Validates against CIS, STIG, SOC2, HIPAA, PCI-DSS

- **🗄️ Database Support**:
  - PostgreSQL (fully implemented)
  - MySQL (planned)
  - Oracle, MongoDB (future)

- **📊 Comprehensive Reports**:
  - JSON (machine-readable)
  - Markdown (human-readable)
  - HTML (web-viewable)

- **🎯 Compliance Frameworks**:
  - CIS Benchmarks
  - DISA STIG
  - SOC 2
  - HIPAA
  - PCI-DSS

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database (for testing)
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

```bash
# Clone the repository
git clone https://github.com/bulump/db-security-scanner.git
cd db-security-scanner

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY and database credentials
```

### Usage

```python
from src.scanner import DatabaseSecurityScanner
from src.reports.generator import ReportGenerator

# Initialize scanner
scanner = DatabaseSecurityScanner()

# Perform scan
report = scanner.scan(
    host='localhost',
    port=5432,
    database='mydb',
    user='postgres',
    password='password',
    compliance_framework='CIS'
)

# Generate report
md_report = ReportGenerator.generate_markdown(report)
print(md_report)
```

### Example Scan

```bash
cd examples
python sample_scan.py
```

This will:
1. Connect to your database
2. Gather configuration and security info
3. Run AI analysis across three agents
4. Generate reports in multiple formats

## 📖 How It Works

### Architecture

```
┌─────────────────────────────────────────────┐
│         Database Security Scanner           │
├─────────────────────────────────────────────┤
│                                             │
│  ┌────────────┐  ┌──────────────┐  ┌─────┐│
│  │ PostgreSQL │  │    MySQL     │  │ ... ││
│  │ Connector  │  │  Connector   │  │     ││
│  └─────┬──────┘  └──────┬───────┘  └─────┘│
│        │                │                  │
│        └────────────────┴──────────────────│
│                    │                       │
│         ┌──────────▼──────────┐           │
│         │  Data Collector     │           │
│         └──────────┬──────────┘           │
│                    │                       │
│         ┌──────────▼──────────┐           │
│         │   AI Agent Layer    │           │
│         ├─────────────────────┤           │
│         │ Config Analyzer     │           │
│         │ Vulnerability       │           │
│         │ Compliance Checker  │           │
│         └──────────┬──────────┘           │
│                    │                       │
│         ┌──────────▼──────────┐           │
│         │  Report Generator   │           │
│         └─────────────────────┘           │
└─────────────────────────────────────────────┘
```

### AI Agent Design

Each agent uses Claude AI with specialized prompts based on 20+ years of database security expertise:

1. **Configuration Analyzer**
   - Analyzes 50+ security-relevant parameters
   - Identifies misconfigurations
   - Provides remediation steps
   - References CVEs when applicable

2. **Vulnerability Detector**
   - Checks database version against known CVEs
   - Identifies excessive privileges
   - Detects weak authentication
   - Assesses exploitability

3. **Compliance Checker**
   - Validates against compliance frameworks
   - Generates pass/fail reports
   - Provides remediation guidance
   - Calculates compliance percentage

## 🎓 Learning Outcomes

This project demonstrates:

- **AI Agent Architecture**: Designing specialized AI agents for domain-specific tasks
- **Prompt Engineering**: Encoding expert knowledge into effective AI prompts
- **Multi-Agent Coordination**: Orchestrating multiple AI agents for comprehensive analysis
- **Real-World Application**: Solving actual security problems with AI
- **Database Security**: Applying 20+ years of expertise to automation

## 🛠️ Tech Stack

- **AI/ML**: Anthropic Claude (claude-sonnet-4)
- **Language**: Python 3.8+
- **Database**: psycopg2, PyMySQL
- **Web**: Flask (for demo interface)
- **Reports**: Markdown, JSON, HTML

## 📈 Project Status

- ✅ Core architecture implemented
- ✅ PostgreSQL connector complete
- ✅ Three AI agents functional
- ✅ Report generation working
- 🚧 Web interface (in progress)
- 📋 MySQL support (planned)
- 📋 PDF reports (planned)

## 🤝 Contributing

This is a learning project showcasing AI/ML skills. Suggestions and improvements welcome!

## 📝 License

MIT License - feel free to use and modify

## 👤 Author

**Chris Bielinski**
- Engineering Manager & Security Technologist
- 20+ years in database security and cloud infrastructure
- [LinkedIn](https://linkedin.com/in/cbielins)
- [GitHub](https://github.com/bulump)
- [Portfolio](https://bulump.github.io)

## 🙏 Acknowledgments

- Built with [Anthropic Claude](https://www.anthropic.com/)
- Inspired by 20+ years of database security experience at Trustwave, Qualys, and IBM
- Part of continuous learning journey into AI and agentic systems

---

*This project demonstrates the intersection of deep domain expertise and modern AI capabilities - showing how traditional security knowledge can be amplified through intelligent automation.*
