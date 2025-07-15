# DevAccess AI PowerShell Wrapper
# This script provides a seamless PowerShell interface for DevAccess AI

param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# Configuration
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$CLI_SCRIPT = Join-Path $SCRIPT_DIR "devaccess-cli.py"
$VENV_DIR = Join-Path $SCRIPT_DIR "venv"
$PYTHON_EXE = Join-Path $VENV_DIR "Scripts\python.exe"

# Color functions
function Write-Success($message) {
    Write-Host "✅ $message" -ForegroundColor Green
}

function Write-Error($message) {
    Write-Host "❌ $message" -ForegroundColor Red
}

function Write-Warning($message) {
    Write-Host "⚠️ $message" -ForegroundColor Yellow
}

function Write-Info($message) {
    Write-Host "ℹ️ $message" -ForegroundColor Cyan
}

# Check if Python is available
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.[8-9]|Python 3\.1[0-9]") {
            return $true
        }
        else {
            Write-Error "Python 3.8+ required. Found: $pythonVersion"
            return $false
        }
    }
    catch {
        Write-Error "Python not found. Please install Python 3.8+ and add it to PATH"
        return $false
    }
}

# Setup virtual environment
function Initialize-Environment {
    Write-Info "Setting up DevAccess AI environment..."
    
    if (-not (Test-Python)) {
        return $false
    }
    
    # Create virtual environment if it doesn't exist
    if (-not (Test-Path $VENV_DIR)) {
        Write-Info "Creating virtual environment..."
        python -m venv $VENV_DIR
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to create virtual environment"
            return $false
        }
    }
    
    # Install requirements
    $requirementsFile = Join-Path $SCRIPT_DIR "cli-requirements.txt"
    
    if (Test-Path $requirementsFile) {
        Write-Info "Installing Python dependencies..."
        & $PYTHON_EXE -m pip install -r $requirementsFile --quiet
        
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install dependencies"
            return $false
        }
    }
    else {
        Write-Info "Installing basic dependencies..."
        & $PYTHON_EXE -m pip install click aiohttp rich pyyaml pandas --quiet
    }
    
    Write-Success "Environment setup complete"
    return $true
}

# Main execution
function Invoke-DevAccess {
    param([string[]]$Args)
    
    # Check if virtual environment exists
    if (-not (Test-Path $PYTHON_EXE)) {
        Write-Warning "DevAccess AI not initialized. Setting up..."
        if (-not (Initialize-Environment)) {
            Write-Error "Failed to initialize environment"
            return
        }
    }
    
    # Check if CLI script exists
    if (-not (Test-Path $CLI_SCRIPT)) {
        Write-Error "CLI script not found: $CLI_SCRIPT"
        return
    }
    
    # Execute the CLI
    try {
        & $PYTHON_EXE $CLI_SCRIPT $Args
    }
    catch {
        Write-Error "Failed to execute DevAccess AI CLI: $_"
    }
}

# Handle special commands
if ($Arguments.Count -eq 0) {
    Write-Host @"
DevAccess AI - PowerShell Interface

Usage:
  devaccess <command> [options]

Commands:
  init                 Initialize DevAccess AI
  health              Check API health
  account create      Create new accounts
  account list        List accounts
  monitor usage       Monitor usage
  software list       List available software
  config set          Set configuration
  config get          Get configuration
  
Examples:
  devaccess init
  devaccess health
  devaccess account create --software cursor,vercel
  devaccess monitor usage --refresh
  devaccess software list --category "Development Tools"

For detailed help:
  devaccess --help
"@
    return
}

# Handle setup command
if ($Arguments[0] -eq "setup") {
    Initialize-Environment
    return
}

# Handle version command
if ($Arguments[0] -eq "version") {
    Write-Host "DevAccess AI CLI v1.0.0"
    Write-Host "PowerShell Wrapper"
    return
}

# Execute the main CLI
Invoke-DevAccess -Args $Arguments
