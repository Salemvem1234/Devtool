"""
DevAccess AI - Integrated Web Application
Combines the beautiful UI with the powerful backend system
"""
import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

# Add the backend to Python path
backend_path = Path(__file__).parent / "devaccess-ai" / "backend"
sys.path.insert(0, str(backend_path))

# Import backend components
from app.core.config import settings
from app.core.database import engine, get_db
from app.models import Base
from app.api.v1.api import api_router
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.services.usage_monitoring_service import UsageMonitoringService

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="DevAccess AI - Integrated Platform",
    description="Full-stack platform for managing free tier development tools with AI assistance",
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="."), name="static")

# Setup templates
templates = Jinja2Templates(directory=".")

# Include API router
app.include_router(api_router, prefix="/api/v1")


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting DevAccess AI Integrated Platform", version="1.0.0")
    
    try:
        # Create database tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
        yield
    finally:
        # Shutdown
        logger.info("Shutting down DevAccess AI Platform")


# Frontend Routes
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """Serve the DevAccess AI homepage"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)


@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/account-details", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the account details dashboard"""
    with open("account-details.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)


@app.get("/create-account", response_class=HTMLResponse)
async def create_account_page(request: Request):
    """Serve the account creation page"""
    with open("create-account.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)


# Enhanced API Endpoints for Frontend Integration
@app.get("/api/frontend/account-data")
async def get_account_data_for_frontend(
    account_id: int = 1,  # Default account for demo
    db: AsyncSession = Depends(get_db)
):
    """Get account data formatted for the frontend dashboard"""
    try:
        # Mock data for demonstration - in production, fetch from database
        account_data = {
            "software_info": {
                "name": "Cursor IDE",
                "logo": "VS",
                "profile_url": "https://cursor.sh"
            },
            "credentials": {
                "email": "dev.user.2025@tempmail.cursor.com",
                "password": "Kx9#mP2$wQ8@vN5!",
                "login_url": "https://cursor.sh/login"
            },
            "status": {
                "active": True,
                "usage_context": "Web Application Development"
            },
            "usage_metrics": [
                {
                    "name": "API Calls",
                    "current": 3780,
                    "limit": 5000,
                    "unit": "calls",
                    "reset_date": "Feb 1st",
                    "status": "normal"
                },
                {
                    "name": "Storage Used",
                    "current": 870,
                    "limit": 1024,
                    "unit": "MB",
                    "reset_date": "Monthly limit",
                    "status": "warning"
                },
                {
                    "name": "Build Minutes",
                    "current": 525,
                    "limit": 500,
                    "unit": "minutes",
                    "reset_date": "Feb 1st",
                    "status": "exceeded"
                },
                {
                    "name": "Team Collaborators",
                    "current": 2,
                    "limit": 5,
                    "unit": "members",
                    "reset_date": "No reset - permanent allocation",
                    "status": "normal"
                }
            ],
            "last_updated": "5 minutes ago"
        }
        
        return account_data
        
    except Exception as e:
        logger.error("Failed to get account data", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get account data")


@app.post("/api/frontend/refresh-usage")
async def refresh_usage_data(
    db: AsyncSession = Depends(get_db)
):
    """Refresh usage data for the frontend"""
    try:
        # Simulate data refresh
        updated_metrics = [
            {
                "name": "API Calls",
                "current": 3785,
                "limit": 5000,
                "unit": "calls",
                "reset_date": "Feb 1st",
                "status": "normal"
            },
            {
                "name": "Storage Used",
                "current": 875,
                "limit": 1024,
                "unit": "MB",
                "reset_date": "Monthly limit",
                "status": "warning"
            },
            {
                "name": "Build Minutes",
                "current": 525,
                "limit": 500,
                "unit": "minutes",
                "reset_date": "Feb 1st",
                "status": "exceeded"
            },
            {
                "name": "Team Collaborators",
                "current": 2,
                "limit": 5,
                "unit": "members",
                "reset_date": "No reset - permanent allocation",
                "status": "normal"
            }
        ]
        
        return {
            "success": True,
            "message": "Usage data refreshed successfully",
            "metrics": updated_metrics,
            "last_updated": "just now"
        }
        
    except Exception as e:
        logger.error("Failed to refresh usage data", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to refresh usage data")


@app.post("/api/frontend/create-accounts")
async def create_accounts_from_frontend(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle account creation requests from the frontend form"""
    try:
        form_data = await request.json()
        
        # Process the form data
        software_list = form_data.get("software", [])
        other_software = form_data.get("otherSoftware", "")
        account_counts = form_data.get("accountCounts", {})
        email_domain = form_data.get("emailDomain", "")
        custom_domain = form_data.get("customDomain", "")
        password_complexity = form_data.get("passwordComplexity", "")
        usage_context = form_data.get("usageContext", "")
        
        # Log the request
        logger.info(
            "Account creation request received",
            software=software_list,
            other_software=other_software,
            account_counts=account_counts,
            email_domain=email_domain,
            usage_context=usage_context
        )
        
        # Mock response for demonstration
        created_accounts = []
        for software in software_list:
            count = account_counts.get(software, 1)
            for i in range(count):
                account = {
                    "id": len(created_accounts) + 1,
                    "software": software,
                    "email": f"user{i+1}.{software}@tempmail.dev",
                    "password": "SecurePassword123!",
                    "status": "created",
                    "login_url": f"https://{software}.com/login"
                }
                created_accounts.append(account)
        
        return {
            "success": True,
            "message": f"Successfully created {len(created_accounts)} accounts",
            "accounts": created_accounts,
            "processing_time": "2.3 seconds"
        }
        
    except Exception as e:
        logger.error("Failed to create accounts", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create accounts")


@app.get("/api/frontend/software-list")
async def get_available_software():
    """Get list of available software for account creation"""
    software_list = [
        {
            "id": "cursor",
            "name": "Cursor IDE",
            "description": "AI-powered code editor",
            "category": "Development Tools",
            "free_tier": {
                "api_calls": 5000,
                "storage": "1GB",
                "features": ["AI assistance", "Code completion", "Debugging"]
            }
        },
        {
            "id": "lovable",
            "name": "Lovable",
            "description": "AI-powered web development platform",
            "category": "Development Platforms",
            "free_tier": {
                "projects": 3,
                "builds": 100,
                "features": ["AI code generation", "Deployment", "Collaboration"]
            }
        },
        {
            "id": "warp",
            "name": "Warp Terminal",
            "description": "Modern, intelligent terminal",
            "category": "Developer Tools",
            "free_tier": {
                "ai_commands": 1000,
                "workflows": 50,
                "features": ["AI command suggestions", "Smart workflows", "Team sharing"]
            }
        },
        {
            "id": "vercel",
            "name": "Vercel",
            "description": "Frontend deployment platform",
            "category": "Deployment",
            "free_tier": {
                "deployments": 100,
                "bandwidth": "100GB",
                "features": ["Edge functions", "Analytics", "Custom domains"]
            }
        },
        {
            "id": "firebase",
            "name": "Firebase",
            "description": "Google's app development platform",
            "category": "Backend Services",
            "free_tier": {
                "reads": 50000,
                "writes": 20000,
                "storage": "1GB",
                "features": ["Authentication", "Realtime database", "Hosting"]
            }
        }
    ]
    
    return {
        "software": software_list,
        "total": len(software_list),
        "categories": list(set([s["category"] for s in software_list]))
    }


# API Health and Info endpoints
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DevAccess AI Integrated Platform",
        "version": "1.0.0",
        "frontend": "enabled",
        "backend": "enabled"
    }


@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "DevAccess AI Platform",
        "version": "1.0.0",
        "description": "Full-stack platform for managing free tier development tools with AI assistance",
        "endpoints": {
            "frontend": ["/", "/dashboard", "/create-account"],
            "api": ["/api/v1/*", "/api/frontend/*", "/api/health", "/api/info"],
            "docs": "/api/docs" if settings.DEBUG else "disabled"
        },
        "features": [
            "Account creation automation",
            "Usage monitoring and alerts",
            "AI-powered recommendations",
            "Real-time dashboard",
            "Free tier optimization"
        ]
    }


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Global HTTP exception handler"""
    logger.error(
        "HTTP Exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors"""
    logger.error(
        "Unexpected error occurred",
        error=str(exc),
        path=request.url.path,
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting DevAccess AI Integrated Platform")
    print("📱 Frontend: http://localhost:8000")
    print("🔧 API Docs: http://localhost:8000/api/docs")
    print("📊 Dashboard: http://localhost:8000/dashboard")
    print("➕ Create Account: http://localhost:8000/create-account")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
