# Setup Guide

## ✅ Installation Complete!

Your AI-Powered Database Security Scanner is ready to use.

## What's Installed:

- ✅ Python 3.12.12 (Homebrew)
- ✅ PostgreSQL 16
- ✅ Virtual environment with all dependencies
- ✅ Test database `testdb`

## Quick Start:

### 1. Get Your Anthropic API Key

1. Go to https://console.anthropic.com/settings/keys
2. Sign up/sign in
3. Create a new API key
4. Copy the key (starts with `sk-ant-api03-...`)

### 2. Configure Environment

```bash
# Copy the example .env file
cp .env.example .env

# Edit .env and add your API key
nano .env
```

Update these values in `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=testdb
DB_USER=cbielins
DB_PASSWORD=
```

### 3. Activate Virtual Environment

```bash
# Always activate the venv before running the scanner
cd ~/git/db-security-scanner
source venv/bin/activate
```

### 4. Run Your First Scan

**Option A: Web Interface (Recommended for Demos)**

```bash
python app.py
```

Then open your browser to http://localhost:5001 and use the interactive web interface!

**Option B: Command Line**

```bash
python examples/sample_scan.py
```

This will:
- Connect to your local PostgreSQL database
- Run AI security analysis
- Generate reports in JSON, Markdown, and HTML formats

## Expected Output:

```
=======================================================================
AI-Powered Database Security Scanner
Combining 20+ years of expertise with modern AI
=======================================================================

🔍 Starting security scan of testdb on localhost:5432
📊 Gathering database information...
✓ Connected to PostgreSQL: PostgreSQL 16.10...

🤖 Running AI Security Analysis...
  → Configuration Analysis...
  → Vulnerability Detection...
  → Compliance Checking...

📄 Generating reports...
  ✓ Markdown report saved to: security_report.md
  ✓ JSON report saved to: security_report.json
  ✓ HTML report saved to: security_report.html

=======================================================================
SCAN SUMMARY
=======================================================================
Security Score: 85/100
Risk Level: MEDIUM
Critical Issues: 2
Vulnerabilities: 1
Compliance: 78%
=======================================================================
```

## Troubleshooting:

### PostgreSQL not running?
```bash
brew services start postgresql@16
```

### Virtual environment issues?
```bash
# Deactivate first if needed
deactivate

# Then reactivate
source venv/bin/activate
```

### Missing API key error?
Make sure you've:
1. Created a `.env` file (not `.env.example`)
2. Added your real API key to it
3. No spaces around the `=` sign

## Daily Usage:

Every time you work on this project:

```bash
cd ~/git/db-security-scanner
source venv/bin/activate
# Now run your commands
python examples/sample_scan.py
```

## Cost Information:

- Each scan costs approximately $0.10-0.30
- Free tier includes $5 in credits (15-50 scans)
- Monitor usage at: https://console.anthropic.com/settings/billing

## Next Steps:

- [ ] Run your first scan (web interface or command line)
- [ ] Review the generated reports
- [ ] Try scanning different databases
- [ ] Modify the agents to customize analysis
- [ ] Explore the web dashboard at http://localhost:5001

## Web Interface Features:

The web interface (`python app.py`) provides:
- 🎨 Beautiful dark-themed dashboard
- 📊 Interactive scan results with real-time progress
- 🎯 Multiple compliance framework selection (CIS, STIG, SOC2, HIPAA, PCI-DSS)
- 📥 Download reports in JSON format
- 🔍 Visual security score and risk level indicators
- 📋 Detailed findings with remediation steps

Enjoy your AI-powered security scanner! 🚀
