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

- **📊 Comprehensive Reports**:
  - PDF (professional, formatted)
  - JSON (machine-readable)
  - Markdown (human-readable)
  - HTML (web-viewable)

- **🎯 Compliance Frameworks**:
  - CIS Benchmarks (PostgreSQL 16 Benchmark v1.1)
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

#### Option 1: Web Interface (Recommended for Demos)

```bash
# Activate virtual environment
source venv/bin/activate

# Start the web server
python app.py
```

Then open your browser to `http://localhost:5001` and use the web interface to:
- Enter database connection details
- Run security scans
- View results in a beautiful, interactive dashboard
- Download JSON reports

#### Option 2: Python API

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

#### Option 3: Command Line Example

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
│         ┌──────────────────────┐            │
│         │  PostgreSQL Connector│            │
│         └──────────┬───────────┘            │
│                    │                        │
│         ┌──────────▼──────────┐             │
│         │  Data Collector     │             │
│         └──────────┬──────────┘             │
│                    │                        │
│         ┌──────────▼──────────┐             │
│         │   AI Agent Layer    │             │
│         ├─────────────────────┤             │
│         │ Config Analyzer     │             │
│         │ Vulnerability       │             │
│         │ Compliance Checker  │             │
│         └──────────┬──────────┘             │
│                    │                        │
│         ┌──────────▼──────────┐             │
│         │  Report Generator   │             │
│         └─────────────────────┘             │
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
   - Validates against compliance frameworks (CIS PostgreSQL 16 Benchmark v1.1)
   - Includes hard-coded validation for 6 critical CIS checks (2.2, 2.3, 2.4, 2.5, 4.2, 4.3)
   - AI-based analysis for broader compliance coverage
   - Generates pass/fail reports with remediation guidance
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
- **Database**: PostgreSQL (psycopg2)
- **Web**: Flask (for demo interface)
- **Reports**: ReportLab (PDF), Markdown, JSON, HTML
- **Testing**: pytest, pytest-cov, pytest-mock

## 🧪 Testing

The project includes a comprehensive test suite with 31 tests covering core functionality:

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html
```

**Test Coverage:**
- ✅ Report generation (PDF, JSON, Markdown, HTML)
- ✅ CIS PostgreSQL 16 Benchmark compliance rules
- ✅ Flask API endpoints
- ✅ Error handling and edge cases

**Current Coverage: 58%** (focusing on critical business logic)

## 📈 Project Status

- ✅ Core architecture implemented
- ✅ PostgreSQL connector complete
- ✅ Three AI agents functional
- ✅ Report generation (PDF, MD, JSON, HTML)
- ✅ Web interface with interactive dashboard
- ✅ CIS PostgreSQL 16 Benchmark v1.1 validation
- ✅ Comprehensive test suite (31 tests, 58% coverage)

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
