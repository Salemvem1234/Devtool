# DevAccess AI CLI - Installation and Usage Guide

## Overview

DevAccess AI CLI is a powerful command-line interface for managing free-tier development tools, creating accounts, monitoring usage, and automating workflows. This guide covers installation, configuration, and usage across different platforms.

## Prerequisites

- **Python 3.8+** (required for CLI)
- **PowerShell 5.1+** (for Windows integration)
- **Chrome/Chromium browser** (for web automation)
- **Active internet connection**

## Installation

### Windows (PowerShell)

1. **Clone/Download the DevAccess AI project:**
   ```powershell
   git clone https://github.com/your-repo/devaccess-ai.git
   cd devaccess-ai
   ```

2. **Set up PowerShell integration:**
   ```powershell
   # Make the PowerShell script executable
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   
   # Test the installation
   .\devaccess.ps1 setup
   ```

3. **Add to PATH (optional):**
   ```powershell
   # Add current directory to PATH for session
   $env:PATH += ";$(Get-Location)"
   
   # Or add permanently to user PATH
   [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$(Get-Location)", [EnvironmentVariableTarget]::User)
   ```

### Linux/macOS

1. **Install Python dependencies:**
   ```bash
   pip install -r cli-requirements.txt
   ```

2. **Make CLI executable:**
   ```bash
   chmod +x devaccess-cli.py
   ```

3. **Create symlink (optional):**
   ```bash
   ln -s $(pwd)/devaccess-cli.py /usr/local/bin/devaccess
   ```

## Configuration

### Initial Setup

1. **Initialize the CLI:**
   ```bash
   devaccess init
   ```

2. **Configure API endpoint:**
   ```bash
   devaccess config set api_url http://localhost:8000
   ```

3. **Test connection:**
   ```bash
   devaccess health
   ```

### Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `api_url` | DevAccess AI API endpoint | `http://localhost:8000` |
| `timeout` | Request timeout in seconds | `30` |
| `max_retries` | Maximum retry attempts | `3` |
| `output_format` | Default output format | `table` |

## Basic Usage

### Account Management

#### Create Accounts
```bash
# Interactive account creation
devaccess account create

# Create specific accounts
devaccess account create --software cursor,vercel --count 2

# Create with specific email domain
devaccess account create --software cursor --email-domain protonmail.com

# Create with usage context
devaccess account create --software vercel --usage-context "Web development project"
```

#### List Accounts
```bash
# List all accounts
devaccess account list

# List specific account
devaccess account list --account-id 1

# Filter by software
devaccess account list --software cursor

# Output as JSON
devaccess account list --format json
```

### Usage Monitoring

#### Check Usage
```bash
# Monitor usage for account
devaccess monitor usage --account-id 1

# Refresh usage data
devaccess monitor usage --refresh

# Output as table with colors
devaccess monitor usage --format table
```

#### View Usage Summary
```bash
# Get usage summary for all accounts
devaccess monitor usage

# Export to file
devaccess monitor usage --output usage-report --format json
```

### Software Management

#### List Available Software
```bash
# List all available software
devaccess software list

# Filter by category
devaccess software list --category "Development Tools"

# Output as YAML
devaccess software list --format yaml
```

#### Check Software Details
```bash
# Get software details
devaccess software list --format json | jq '.[] | select(.name=="Cursor")'
```

### Configuration Management

#### Set Configuration
```bash
# Set API URL
devaccess config set api_url https://api.devaccess.ai

# Set timeout
devaccess config set timeout 60

# Set default output format
devaccess config set output_format json
```

#### Get Configuration
```bash
# Get all configuration
devaccess config get

# Get specific value
devaccess config get api_url
```

## Advanced Usage

### Batch Operations

#### Create Multiple Accounts
```bash
# Create accounts for multiple software
devaccess account create --software "cursor,vercel,firebase" --count 2

# Create with different contexts
devaccess account create --software cursor --usage-context "Development testing"
```

#### Automated Workflows
```bash
# Create and monitor in sequence
devaccess account create --software cursor --count 1
devaccess monitor usage --account-id 1 --refresh
```

### Output Formats

#### JSON Output
```bash
devaccess account list --format json | jq '.'
```

#### YAML Output
```bash
devaccess software list --format yaml
```

#### CSV Export
```bash
devaccess monitor usage --format csv --output usage-data
```

### Integration Examples

#### PowerShell Integration
```powershell
# Get account data and process with PowerShell
$accounts = devaccess account list --format json | ConvertFrom-Json
$accounts | Where-Object { $_.software -eq "cursor" }
```

#### Bash Integration
```bash
# Get usage and alert if high
usage=$(devaccess monitor usage --format json | jq '.[] | select(.status=="warning")')
if [ -n "$usage" ]; then
    echo "Warning: Usage limits approaching!"
fi
```

## Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Install Python 3.8+
# Windows: Download from python.org
# Linux: sudo apt install python3.8
# macOS: brew install python@3.8
```

#### Permission Errors (Windows)
```powershell
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Connection Errors
```bash
# Check API health
devaccess health

# Verify API URL
devaccess config get api_url

# Test with curl
curl http://localhost:8000/api/health
```

#### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows
pip install -r cli-requirements.txt
```

### Debug Mode

Enable debug mode for detailed output:
```bash
devaccess --debug account create --software cursor
```

### Logs and Configuration

- **Configuration Directory**: `~/.devaccess/`
- **Config File**: `~/.devaccess/config.ini`
- **Output Directory**: `~/.devaccess/outputs/`
- **Logs**: Console output (can be redirected)

## API Integration

### Using with CI/CD

#### GitHub Actions Example
```yaml
name: DevAccess Account Management
on:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  manage-accounts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install CLI
        run: pip install -r cli-requirements.txt
      - name: Check Usage
        run: python devaccess-cli.py monitor usage --format json
```

#### PowerShell Script Example
```powershell
# Daily usage monitoring script
$usage = devaccess monitor usage --format json | ConvertFrom-Json
$warnings = $usage | Where-Object { $_.status -eq "warning" }

if ($warnings.Count -gt 0) {
    Write-Host "⚠️ Usage warnings detected:" -ForegroundColor Yellow
    $warnings | ForEach-Object { Write-Host "  - $($_.name): $($_.current)/$($_.limit)" }
}
```

## Best Practices

### Security
- Store sensitive configuration in environment variables
- Use temporary email domains for testing
- Regularly rotate generated passwords
- Monitor account usage to prevent abuse

### Performance
- Use batch operations for multiple accounts
- Cache configuration locally
- Use appropriate timeouts for automation
- Monitor API rate limits

### Automation
- Set up regular usage monitoring
- Use webhooks for real-time alerts
- Implement retry logic for failed operations
- Log automation results for audit trails

## Support and Contributing

- **Issues**: Report bugs on GitHub
- **Documentation**: Contribute to docs
- **Features**: Submit feature requests
- **Code**: Submit pull requests

## Examples Repository

Check the `examples/` directory for:
- PowerShell automation scripts
- Bash integration examples
- CI/CD configuration files
- Advanced usage patterns

---

**DevAccess AI CLI** - Making development tool management effortless!
