# DevAccess AI Setup Script for Windows
Write-Host "Setting up DevAccess AI Development Environment..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install Python 3.11+ first." -ForegroundColor Red
    exit 1
}

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Create Python virtual environment
Write-Host "`nCreating Python virtual environment..." -ForegroundColor Yellow
Set-Location "backend"

if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping creation." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "`nActivating virtual environment and installing dependencies..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
Write-Host "`nDownloading spaCy NLP model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm

# Install Playwright browsers
Write-Host "`nInstalling Playwright browsers..." -ForegroundColor Yellow
playwright install chromium

Write-Host "`nBackend dependencies installed successfully!" -ForegroundColor Green

# Go back to root directory
Set-Location ".."

# Create environment file
Write-Host "`nSetting up environment configuration..." -ForegroundColor Yellow
if (Test-Path "backend\.env") {
    Write-Host "Environment file already exists, skipping creation." -ForegroundColor Yellow
} else {
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "Environment file created from template" -ForegroundColor Green
    Write-Host "Please edit backend\.env and update the configuration values" -ForegroundColor Yellow
}

# Generate secret keys
Write-Host "`nGenerating secure keys..." -ForegroundColor Yellow
$secretKey = [System.Web.Security.Membership]::GeneratePassword(64, 20)
$encryptionKey = [System.Web.Security.Membership]::GeneratePassword(32, 10)

Write-Host "Generated SECRET_KEY: $secretKey" -ForegroundColor Cyan
Write-Host "Generated ENCRYPTION_KEY: $encryptionKey" -ForegroundColor Cyan
Write-Host "Please update these in your .env file" -ForegroundColor Yellow

# Docker setup
Write-Host "`nStarting Docker services..." -ForegroundColor Yellow
docker-compose up -d postgres redis

Write-Host "`nWaiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "`nDevAccess AI setup completed!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor White
Write-Host "1. Update backend\.env with your configuration values" -ForegroundColor White
Write-Host "2. Run: docker-compose up -d (to start all services)" -ForegroundColor White
Write-Host "3. Visit: http://localhost:8000/docs (API documentation)" -ForegroundColor White
Write-Host "4. Visit: http://localhost:8000/health (health check)" -ForegroundColor White

Write-Host "`nUseful commands:" -ForegroundColor White
Write-Host "- Start services: docker-compose up -d" -ForegroundColor Gray
Write-Host "- Stop services: docker-compose down" -ForegroundColor Gray
Write-Host "- View logs: docker-compose logs -f backend" -ForegroundColor Gray
Write-Host "- Run backend locally: cd backend, then venv\Scripts\Activate.ps1, then uvicorn app.main:app" -ForegroundColor Gray
