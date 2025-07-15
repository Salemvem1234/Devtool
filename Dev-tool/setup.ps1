# DevAccess AI - Quick Setup Script
# This script sets up DevAccess AI with all dependencies

[CmdletBinding()]
param(
    [switch]$SkipPython,
    [switch]$SkipDependencies,
    [switch]$Force
)

# Colors for output
function Write-Success($message) { Write-Host "✅ $message" -ForegroundColor Green }
function Write-Error($message) { Write-Host "❌ $message" -ForegroundColor Red }
function Write-Warning($message) { Write-Host "⚠️ $message" -ForegroundColor Yellow }
function Write-Info($message) { Write-Host "ℹ️ $message" -ForegroundColor Cyan }
function Write-Step($message) { Write-Host "🔄 $message" -ForegroundColor Blue }

Write-Host @"
╔════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                            ║
║                               🚀 DevAccess AI Setup                                       ║
║                                                                                            ║
║        Intelligent CLI for Managing Free-Tier Development Tools                           ║
║                                                                                            ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    Write-Warning "Running as Administrator. Some features may not work correctly."
    if (-not $Force) {
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -notmatch "^[yY]") {
            Write-Error "Setup cancelled."
            exit 1
        }
    }
}

# Configuration
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VENV_DIR = Join-Path $SCRIPT_DIR "venv"
$REQUIREMENTS_FILE = Join-Path $SCRIPT_DIR "cli-requirements.txt"
$CLI_SCRIPT = Join-Path $SCRIPT_DIR "devaccess-cli.py"
$PS_WRAPPER = Join-Path $SCRIPT_DIR "devaccess.ps1"

# Step 1: Check Python Installation
Write-Step "Checking Python installation..."

if (-not $SkipPython) {
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "Found Python: $pythonVersion"
        
        if ($pythonVersion -match "Python 3\.[8-9]|Python 3\.1[0-9]") {
            Write-Success "Python version is compatible"
        } else {
            Write-Error "Python 3.8+ required. Found: $pythonVersion"
            Write-Info "Please install Python 3.8+ from https://python.org"
            exit 1
        }
    }
    catch {
        Write-Error "Python not found. Please install Python 3.8+ and add it to PATH"
        Write-Info "Download from: https://python.org"
        exit 1
    }
} else {
    Write-Info "Skipping Python check"
}

# Step 2: Create Virtual Environment
Write-Step "Setting up virtual environment..."

if (Test-Path $VENV_DIR) {
    Write-Warning "Virtual environment already exists"
    if ($Force) {
        Write-Info "Removing existing virtual environment"
        Remove-Item $VENV_DIR -Recurse -Force
    } else {
        $recreate = Read-Host "Recreate virtual environment? (y/N)"
        if ($recreate -match "^[yY]") {
            Remove-Item $VENV_DIR -Recurse -Force
        }
    }
}

if (-not (Test-Path $VENV_DIR)) {
    Write-Info "Creating virtual environment..."
    python -m venv $VENV_DIR
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment"
        exit 1
    }
    Write-Success "Virtual environment created"
}

# Step 3: Install Dependencies
Write-Step "Installing Python dependencies..."

$PYTHON_EXE = Join-Path $VENV_DIR "Scripts\python.exe"
$PIP_EXE = Join-Path $VENV_DIR "Scripts\pip.exe"

if (-not $SkipDependencies) {
    # Upgrade pip first
    Write-Info "Upgrading pip..."
    & $PYTHON_EXE -m pip install --upgrade pip --quiet
    
    # Install requirements
    if (Test-Path $REQUIREMENTS_FILE) {
        Write-Info "Installing from requirements file..."
        & $PIP_EXE install -r $REQUIREMENTS_FILE --quiet
    } else {
        Write-Info "Installing basic dependencies..."
        & $PIP_EXE install click aiohttp rich pyyaml pandas configparser --quiet
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install dependencies"
        exit 1
    }
    Write-Success "Dependencies installed"
} else {
    Write-Info "Skipping dependency installation"
}

# Step 4: Verify Installation
Write-Step "Verifying installation..."

if (-not (Test-Path $CLI_SCRIPT)) {
    Write-Error "CLI script not found: $CLI_SCRIPT"
    exit 1
}

if (-not (Test-Path $PS_WRAPPER)) {
    Write-Error "PowerShell wrapper not found: $PS_WRAPPER"
    exit 1
}

# Test the CLI
Write-Info "Testing CLI functionality..."
try {
    & $PYTHON_EXE $CLI_SCRIPT --help | Out-Null
    Write-Success "CLI is working correctly"
} catch {
    Write-Error "CLI test failed: $_"
    exit 1
}

# Step 5: Configure PowerShell Execution Policy
Write-Step "Configuring PowerShell execution policy..."

$currentPolicy = Get-ExecutionPolicy -Scope CurrentUser
if ($currentPolicy -eq "Restricted") {
    Write-Info "Setting execution policy to RemoteSigned for current user"
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Success "Execution policy updated"
    } catch {
        Write-Warning "Could not update execution policy: $_"
        Write-Info "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    }
} else {
    Write-Success "Execution policy is already configured"
}

# Step 6: Test PowerShell Integration
Write-Step "Testing PowerShell integration..."

try {
    & $PS_WRAPPER version
    Write-Success "PowerShell integration is working"
} catch {
    Write-Error "PowerShell integration test failed: $_"
    Write-Info "You may need to run the script manually: .\devaccess.ps1"
}

# Step 7: Create Desktop Shortcut (Optional)
Write-Step "Creating shortcuts..."

$createShortcut = Read-Host "Create desktop shortcut? (y/N)"
if ($createShortcut -match "^[yY]") {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "DevAccess AI.lnk"
    
    $WScriptShell = New-Object -ComObject WScript.Shell
    $shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = "powershell.exe"
    $shortcut.Arguments = "-NoExit -ExecutionPolicy Bypass -File `"$PS_WRAPPER`""
    $shortcut.WorkingDirectory = $SCRIPT_DIR
    $shortcut.Description = "DevAccess AI CLI"
    $shortcut.Save()
    
    Write-Success "Desktop shortcut created"
}

# Step 8: Add to PATH (Optional)
Write-Step "Configuring PATH..."

$currentPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
if ($currentPath -notlike "*$SCRIPT_DIR*") {
    $addToPath = Read-Host "Add to user PATH? (y/N)"
    if ($addToPath -match "^[yY]") {
        $newPath = "$currentPath;$SCRIPT_DIR"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::User)
        Write-Success "Added to user PATH"
        Write-Info "Restart your terminal to use 'devaccess' command globally"
    }
} else {
    Write-Success "Already in PATH"
}

# Step 9: Final Configuration
Write-Step "Final configuration..."

# Create config directory
$configDir = Join-Path $env:USERPROFILE ".devaccess"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir | Out-Null
    Write-Success "Created configuration directory: $configDir"
}

# Initialize CLI
Write-Info "Initializing DevAccess AI CLI..."
try {
    & $PYTHON_EXE $CLI_SCRIPT init --api-url "http://localhost:8000" 2>&1 | Out-Null
    Write-Success "CLI initialized with default configuration"
} catch {
    Write-Warning "CLI initialization failed (this is normal for first run)"
}

# Success Message
Write-Host @"

╔════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                            ║
║                            🎉 Setup Complete! 🎉                                          ║
║                                                                                            ║
║  DevAccess AI CLI is now ready to use!                                                    ║
║                                                                                            ║
║  Next Steps:                                                                               ║
║  1. Start the DevAccess AI backend:                                                       ║
║     python app.py                                                                         ║
║                                                                                            ║
║  2. Test the CLI:                                                                         ║
║     .\devaccess.ps1 health                                                                ║
║                                                                                            ║
║  3. Create your first account:                                                            ║
║     .\devaccess.ps1 account create                                                        ║
║                                                                                            ║
║  4. Monitor usage:                                                                        ║
║     .\devaccess.ps1 monitor usage                                                         ║
║                                                                                            ║
║  Documentation: CLI_GUIDE.md                                                              ║
║                                                                                            ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Green

# Additional Information
Write-Info "Configuration Details:"
Write-Host "  📁 Installation Directory: $SCRIPT_DIR"
Write-Host "  🐍 Python Virtual Environment: $VENV_DIR"
Write-Host "  ⚙️ Configuration Directory: $configDir"
Write-Host "  📜 PowerShell Wrapper: $PS_WRAPPER"
Write-Host "  🔧 CLI Script: $CLI_SCRIPT"

Write-Info "Quick Commands:"
Write-Host "  devaccess --help          # Show help"
Write-Host "  devaccess health          # Check API health"
Write-Host "  devaccess account create  # Create accounts"
Write-Host "  devaccess monitor usage   # Monitor usage"
Write-Host "  devaccess software list   # List available software"

Write-Success "Setup completed successfully! 🚀"
