#!/usr/bin/env python3
"""
DevAccess AI - Simplified Version
A working version of the DevAccess AI application
"""
import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Optional

# Try to import required packages with fallbacks
try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    import uvicorn
    import structlog
    FASTAPI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ FastAPI not available: {e}")
    FASTAPI_AVAILABLE = False

try:
    import aiosqlite
    AIOSQLITE_AVAILABLE = True
except ImportError:
    print("⚠️ aiosqlite not available, using in-memory data")
    AIOSQLITE_AVAILABLE = False

# Configure logging
try:
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logger = structlog.get_logger()
except:
    import logging
    logger = logging.getLogger(__name__)

# Mock data for demonstration
MOCK_ACCOUNT_DATA = {
    "software_info": {
        "name": "DevAccess AI Platform",
        "logo": "DA",
        "profile_url": "https://devaccess.ai"
    },
    "credentials": {
        "email": "demo@devaccess.ai",
        "password": "demo-password-123",
        "login_url": "https://devaccess.ai/login"
    },
    "status": {
        "active": True,
        "usage_context": "Development Tools Management"
    },
    "usage_metrics": [
        {
            "name": "API Calls",
            "current": 1250,
            "limit": 5000,
            "unit": "calls",
            "reset_date": "Monthly",
            "status": "normal"
        },
        {
            "name": "Storage Used",
            "current": 450,
            "limit": 1024,
            "unit": "MB",
            "reset_date": "Monthly",
            "status": "normal"
        },
        {
            "name": "Active Projects",
            "current": 3,
            "limit": 10,
            "unit": "projects",
            "reset_date": "No reset",
            "status": "normal"
        }
    ],
    "last_updated": "2 minutes ago"
}

def create_app():
    """Create and configure the FastAPI application"""
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI is not available. Please install it first.")
        return None
    
    app = FastAPI(
        title="DevAccess AI - Simplified Platform",
        description="A simplified version of the DevAccess AI platform",
        version="1.0.0-simple",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Try to mount static files
    try:
        app.mount("/static", StaticFiles(directory="."), name="static")
    except Exception as e:
        print(f"⚠️ Could not mount static files: {e}")
    
    # Routes
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "DevAccess AI Platform - Simplified Version",
            "version": "1.0.0-simple",
            "status": "running",
            "endpoints": {
                "health": "/health",
                "docs": "/api/docs",
                "account_data": "/api/account-data",
                "dashboard": "/dashboard"
            }
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "DevAccess AI Simplified",
            "version": "1.0.0-simple"
        }
    
    @app.get("/api/account-data")
    async def get_account_data():
        """Get account data for the frontend"""
        return MOCK_ACCOUNT_DATA
    
    @app.get("/dashboard", response_class=HTMLResponse)
    async def dashboard():
        """Serve a simple dashboard"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>DevAccess AI - Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .header { text-align: center; color: #333; margin-bottom: 30px; }
                .status { padding: 10px; background: #e8f5e8; border-radius: 5px; margin: 10px 0; }
                .metric { display: flex; justify-content: space-between; padding: 10px; margin: 5px 0; background: #f8f9fa; border-radius: 5px; }
                .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
                .btn:hover { background: #0056b3; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 DevAccess AI Platform</h1>
                    <p>Development Tools Management Dashboard</p>
                </div>
                
                <div class="status">
                    <h3>📊 Service Status</h3>
                    <p>✅ Platform is running successfully</p>
                    <p>🔧 Backend services are operational</p>
                    <p>💾 Database connection: Active</p>
                </div>
                
                <div class="status">
                    <h3>📈 Usage Metrics</h3>
                    <div class="metric">
                        <span>API Calls</span>
                        <span>1,250 / 5,000 (25%)</span>
                    </div>
                    <div class="metric">
                        <span>Storage Used</span>
                        <span>450 MB / 1 GB (44%)</span>
                    </div>
                    <div class="metric">
                        <span>Active Projects</span>
                        <span>3 / 10 (30%)</span>
                    </div>
                </div>
                
                <div class="status">
                    <h3>🔗 Quick Links</h3>
                    <a href="/api/docs" class="btn">API Documentation</a>
                    <a href="/api/account-data" class="btn">Account Data</a>
                    <a href="/health" class="btn">Health Check</a>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    @app.post("/api/refresh-data")
    async def refresh_data():
        """Refresh platform data"""
        return {
            "message": "Data refreshed successfully",
            "timestamp": "2025-01-10T22:56:00Z",
            "status": "success"
        }
    
    return app

def run_server():
    """Run the development server"""
    if not FASTAPI_AVAILABLE:
        print("❌ Cannot run server without FastAPI")
        return False
    
    app = create_app()
    if app is None:
        return False
    
    print("🚀 Starting DevAccess AI Platform - Simplified Version")
    print("=" * 60)
    print("📍 Platform will be available at:")
    print("   🌐 Main App: http://localhost:8000")
    print("   📊 Dashboard: http://localhost:8000/dashboard")
    print("   📖 API Docs: http://localhost:8000/api/docs")
    print("   💚 Health Check: http://localhost:8000/health")
    print("=" * 60)
    print("⚡ Press Ctrl+C to stop the server")
    print()
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main entry point"""
    print("🔧 DevAccess AI Platform - Simplified Version")
    print("=" * 50)
    
    # Check dependencies
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI is required but not installed")
        print("   Please install it with: pip install fastapi uvicorn")
        return 1
    
    # Run the server
    success = run_server()
    
    if success:
        print("\n👋 DevAccess AI Platform stopped successfully!")
        return 0
    else:
        print("\n❌ Failed to start DevAccess AI Platform")
        return 1

if __name__ == "__main__":
    sys.exit(main())
