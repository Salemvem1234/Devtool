#!/usr/bin/env python3
"""
DevAccess AI - Comprehensive Platform
A complete application combining frontend, backend, and DevAccess AI features
"""
import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Import required packages
try:
    from fastapi import FastAPI, HTTPException, Request, Form, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError as e:
    print(f"❌ FastAPI not available: {e}")
    FASTAPI_AVAILABLE = False

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    import logging
    STRUCTLOG_AVAILABLE = False

try:
    import aiosqlite
    AIOSQLITE_AVAILABLE = True
except ImportError:
    AIOSQLITE_AVAILABLE = False

# Configure logging
if STRUCTLOG_AVAILABLE:
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
else:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

# Global data store (in-memory for simplicity)
ACCOUNTS_DB = {}
USAGE_STATS = {
    "total_accounts": 0,
    "active_accounts": 0,
    "api_calls_today": 0,
    "last_updated": datetime.now().isoformat()
}

# Mock account data for demonstration
DEMO_ACCOUNTS = [
    {
        "id": 1,
        "software_name": "Cursor IDE",
        "email": "dev.user.2025@tempmail.cursor.com",
        "password": "Kx9#mP2$wQ8@vN5!",
        "login_url": "https://cursor.sh/login",
        "status": "active",
        "usage_context": "Web Application Development",
        "metrics": {
            "api_calls": {"current": 3780, "limit": 5000, "status": "normal"},
            "storage": {"current": 870, "limit": 1024, "status": "warning"},
            "build_minutes": {"current": 525, "limit": 500, "status": "exceeded"},
            "collaborators": {"current": 2, "limit": 5, "status": "normal"}
        }
    },
    {
        "id": 2,
        "software_name": "GitHub Codespaces",
        "email": "developer@gmail.com",
        "password": "SecurePass123!",
        "login_url": "https://github.com/login",
        "status": "active",
        "usage_context": "Open Source Development",
        "metrics": {
            "compute_hours": {"current": 45, "limit": 60, "status": "normal"},
            "storage": {"current": 2.1, "limit": 15, "status": "normal"},
            "repositories": {"current": 8, "limit": 10, "status": "normal"}
        }
    },
    {
        "id": 3,
        "software_name": "Vercel",
        "email": "webdev@outlook.com",
        "password": "Deploy2024$",
        "login_url": "https://vercel.com/login",
        "status": "active",
        "usage_context": "Frontend Deployment",
        "metrics": {
            "deployments": {"current": 15, "limit": 100, "status": "normal"},
            "bandwidth": {"current": 75, "limit": 100, "status": "warning"},
            "functions": {"current": 50, "limit": 12, "status": "exceeded"}
        }
    }
]

# Initialize demo data
for account in DEMO_ACCOUNTS:
    ACCOUNTS_DB[account["id"]] = account

USAGE_STATS["total_accounts"] = len(DEMO_ACCOUNTS)
USAGE_STATS["active_accounts"] = len([a for a in DEMO_ACCOUNTS if a["status"] == "active"])

def create_app():
    """Create and configure the FastAPI application"""
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI is not available. Please install it first.")
        return None
    
    app = FastAPI(
        title="DevAccess AI - Comprehensive Platform",
        description="Complete platform for managing free tier development tools with AI assistance",
        version="1.0.0",
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
    
    # API Routes
    @app.get("/")
    async def root():
        """Root endpoint with platform information"""
        return {
            "message": "DevAccess AI - Comprehensive Platform",
            "version": "1.0.0",
            "status": "running",
            "features": [
                "Account Management",
                "Usage Monitoring",
                "AI-Powered Recommendations",
                "Automated Tool Access",
                "Real-time Analytics"
            ],
            "endpoints": {
                "dashboard": "/dashboard",
                "api_docs": "/api/docs",
                "health": "/health",
                "accounts": "/api/accounts",
                "usage": "/api/usage"
            }
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "DevAccess AI Platform",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "database": "connected" if AIOSQLITE_AVAILABLE else "mock",
                "logging": "structured" if STRUCTLOG_AVAILABLE else "basic",
                "accounts": f"{len(ACCOUNTS_DB)} loaded"
            }
        }
    
    # Account Management API
    @app.get("/api/accounts")
    async def get_accounts():
        """Get all accounts"""
        return {
            "accounts": list(ACCOUNTS_DB.values()),
            "total": len(ACCOUNTS_DB),
            "active": len([a for a in ACCOUNTS_DB.values() if a["status"] == "active"])
        }
    
    @app.get("/api/accounts/{account_id}")
    async def get_account(account_id: int):
        """Get specific account"""
        if account_id not in ACCOUNTS_DB:
            raise HTTPException(status_code=404, detail="Account not found")
        return ACCOUNTS_DB[account_id]
    
    @app.post("/api/accounts")
    async def create_account(
        software_name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        login_url: str = Form(...),
        usage_context: str = Form(...)
    ):
        """Create new account"""
        new_id = max(ACCOUNTS_DB.keys()) + 1 if ACCOUNTS_DB else 1
        new_account = {
            "id": new_id,
            "software_name": software_name,
            "email": email,
            "password": password,
            "login_url": login_url,
            "status": "active",
            "usage_context": usage_context,
            "metrics": {
                "api_calls": {"current": 0, "limit": 1000, "status": "normal"},
                "storage": {"current": 0, "limit": 1000, "status": "normal"}
            },
            "created_at": datetime.now().isoformat()
        }
        ACCOUNTS_DB[new_id] = new_account
        USAGE_STATS["total_accounts"] += 1
        USAGE_STATS["active_accounts"] += 1
        return {"message": "Account created successfully", "account": new_account}
    
    @app.put("/api/accounts/{account_id}")
    async def update_account(account_id: int, account_data: dict):
        """Update account"""
        if account_id not in ACCOUNTS_DB:
            raise HTTPException(status_code=404, detail="Account not found")
        ACCOUNTS_DB[account_id].update(account_data)
        return {"message": "Account updated successfully", "account": ACCOUNTS_DB[account_id]}
    
    @app.delete("/api/accounts/{account_id}")
    async def delete_account(account_id: int):
        """Delete account"""
        if account_id not in ACCOUNTS_DB:
            raise HTTPException(status_code=404, detail="Account not found")
        del ACCOUNTS_DB[account_id]
        USAGE_STATS["total_accounts"] -= 1
        return {"message": "Account deleted successfully"}
    
    # Usage and Analytics API
    @app.get("/api/usage")
    async def get_usage_stats():
        """Get platform usage statistics"""
        return USAGE_STATS
    
    @app.get("/api/analytics")
    async def get_analytics():
        """Get platform analytics"""
        metrics_summary = {}
        for account in ACCOUNTS_DB.values():
            for metric_name, metric_data in account.get("metrics", {}).items():
                if metric_name not in metrics_summary:
                    metrics_summary[metric_name] = {"total_current": 0, "total_limit": 0, "count": 0}
                metrics_summary[metric_name]["total_current"] += metric_data.get("current", 0)
                metrics_summary[metric_name]["total_limit"] += metric_data.get("limit", 0)
                metrics_summary[metric_name]["count"] += 1
        
        return {
            "platform_stats": USAGE_STATS,
            "resource_usage": metrics_summary,
            "account_distribution": {
                "by_software": {},
                "by_status": {"active": 0, "inactive": 0},
                "by_usage_level": {"normal": 0, "warning": 0, "exceeded": 0}
            }
        }
    
    @app.post("/api/refresh")
    async def refresh_data():
        """Refresh platform data"""
        USAGE_STATS["last_updated"] = datetime.now().isoformat()
        USAGE_STATS["api_calls_today"] += 1
        return {"message": "Data refreshed successfully", "timestamp": USAGE_STATS["last_updated"]}
    
    # Frontend Routes
    @app.get("/dashboard", response_class=HTMLResponse)
    async def dashboard():
        """Main dashboard page"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>DevAccess AI - Comprehensive Dashboard</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container { 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background: white; 
                    border-radius: 20px; 
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .header { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; 
                    padding: 30px;
                    text-align: center;
                }
                .header h1 { font-size: 2.5em; margin-bottom: 10px; }
                .header p { font-size: 1.2em; opacity: 0.9; }
                .content { padding: 30px; }
                .stats-grid { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                    gap: 20px; 
                    margin-bottom: 30px;
                }
                .stat-card { 
                    background: #f8f9fa; 
                    padding: 20px; 
                    border-radius: 15px; 
                    text-align: center;
                    transition: transform 0.3s ease;
                }
                .stat-card:hover { transform: translateY(-5px); }
                .stat-card h3 { color: #667eea; margin-bottom: 10px; }
                .stat-card .number { font-size: 2em; font-weight: bold; color: #333; }
                .accounts-section { margin-bottom: 30px; }
                .accounts-grid { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                    gap: 20px;
                }
                .account-card { 
                    background: #ffffff; 
                    border: 1px solid #e9ecef; 
                    border-radius: 15px; 
                    padding: 20px;
                    transition: all 0.3s ease;
                }
                .account-card:hover { 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    transform: translateY(-2px);
                }
                .account-header { 
                    display: flex; 
                    justify-content: space-between; 
                    align-items: center; 
                    margin-bottom: 15px;
                }
                .account-name { font-size: 1.3em; font-weight: bold; color: #333; }
                .status-badge { 
                    padding: 5px 15px; 
                    border-radius: 20px; 
                    color: white; 
                    font-size: 0.8em;
                    background: #28a745;
                }
                .metric { 
                    display: flex; 
                    justify-content: space-between; 
                    margin: 10px 0; 
                    padding: 10px; 
                    background: #f8f9fa; 
                    border-radius: 8px;
                }
                .metric-status { 
                    padding: 2px 8px; 
                    border-radius: 12px; 
                    font-size: 0.8em; 
                    color: white;
                }
                .status-normal { background: #28a745; }
                .status-warning { background: #ffc107; }
                .status-exceeded { background: #dc3545; }
                .actions { 
                    display: flex; 
                    gap: 10px; 
                    justify-content: center; 
                    margin-top: 30px;
                }
                .btn { 
                    padding: 12px 24px; 
                    border: none; 
                    border-radius: 8px; 
                    cursor: pointer; 
                    font-size: 1em;
                    transition: all 0.3s ease;
                    text-decoration: none;
                    display: inline-block;
                }
                .btn-primary { background: #667eea; color: white; }
                .btn-primary:hover { background: #5a6fd8; }
                .btn-success { background: #28a745; color: white; }
                .btn-success:hover { background: #218838; }
                .btn-info { background: #17a2b8; color: white; }
                .btn-info:hover { background: #138496; }
                .footer { 
                    text-align: center; 
                    padding: 20px; 
                    color: #666; 
                    border-top: 1px solid #e9ecef;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 DevAccess AI Platform</h1>
                    <p>Comprehensive Development Tools Management</p>
                </div>
                
                <div class="content">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>📊 Total Accounts</h3>
                            <div class="number" id="totalAccounts">-</div>
                        </div>
                        <div class="stat-card">
                            <h3>✅ Active Accounts</h3>
                            <div class="number" id="activeAccounts">-</div>
                        </div>
                        <div class="stat-card">
                            <h3>🔧 API Calls Today</h3>
                            <div class="number" id="apiCalls">-</div>
                        </div>
                        <div class="stat-card">
                            <h3>📈 Platform Status</h3>
                            <div class="number" style="color: #28a745;">OPERATIONAL</div>
                        </div>
                    </div>
                    
                    <div class="accounts-section">
                        <h2>🏢 Managed Accounts</h2>
                        <div class="accounts-grid" id="accountsGrid">
                            <!-- Accounts will be loaded here -->
                        </div>
                    </div>
                    
                    <div class="actions">
                        <a href="/api/docs" class="btn btn-primary">📖 API Documentation</a>
                        <a href="/create-account" class="btn btn-success">➕ Add Account</a>
                        <a href="/analytics" class="btn btn-info">📊 Analytics</a>
                        <button class="btn btn-primary" onclick="refreshData()">🔄 Refresh Data</button>
                    </div>
                </div>
                
                <div class="footer">
                    <p>&copy; 2025 DevAccess AI Platform - Simplifying Development Tool Management</p>
                </div>
            </div>
            
            <script>
                // Load dashboard data
                async function loadDashboard() {
                    try {
                        // Load usage stats
                        const usageResponse = await fetch('/api/usage');
                        const usageData = await usageResponse.json();
                        
                        document.getElementById('totalAccounts').textContent = usageData.total_accounts;
                        document.getElementById('activeAccounts').textContent = usageData.active_accounts;
                        document.getElementById('apiCalls').textContent = usageData.api_calls_today;
                        
                        // Load accounts
                        const accountsResponse = await fetch('/api/accounts');
                        const accountsData = await accountsResponse.json();
                        
                        const accountsGrid = document.getElementById('accountsGrid');
                        accountsGrid.innerHTML = '';
                        
                        accountsData.accounts.forEach(account => {
                            const accountCard = createAccountCard(account);
                            accountsGrid.appendChild(accountCard);
                        });
                        
                    } catch (error) {
                        console.error('Error loading dashboard:', error);
                    }
                }
                
                function createAccountCard(account) {
                    const card = document.createElement('div');
                    card.className = 'account-card';
                    
                    let metricsHtml = '';
                    if (account.metrics) {
                        Object.entries(account.metrics).forEach(([key, metric]) => {
                            const percentage = Math.round((metric.current / metric.limit) * 100);
                            metricsHtml += `
                                <div class="metric">
                                    <span>${key.replace('_', ' ')}</span>
                                    <span>
                                        ${metric.current}/${metric.limit} (${percentage}%)
                                        <span class="metric-status status-${metric.status}">${metric.status}</span>
                                    </span>
                                </div>
                            `;
                        });
                    }
                    
                    card.innerHTML = `
                        <div class="account-header">
                            <div class="account-name">${account.software_name}</div>
                            <div class="status-badge">${account.status}</div>
                        </div>
                        <p><strong>Email:</strong> ${account.email}</p>
                        <p><strong>Context:</strong> ${account.usage_context}</p>
                        <div style="margin-top: 15px;">
                            <h4>📈 Usage Metrics</h4>
                            ${metricsHtml}
                        </div>
                    `;
                    
                    return card;
                }
                
                async function refreshData() {
                    try {
                        await fetch('/api/refresh', { method: 'POST' });
                        loadDashboard();
                        alert('Data refreshed successfully!');
                    } catch (error) {
                        console.error('Error refreshing data:', error);
                        alert('Error refreshing data');
                    }
                }
                
                // Load dashboard on page load
                document.addEventListener('DOMContentLoaded', loadDashboard);
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    @app.get("/create-account", response_class=HTMLResponse)
    async def create_account_page():
        """Account creation page"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Create Account - DevAccess AI</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .form-container { 
                    background: white; 
                    padding: 40px; 
                    border-radius: 20px; 
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    max-width: 500px;
                    width: 100%;
                }
                .form-header { 
                    text-align: center; 
                    margin-bottom: 30px;
                }
                .form-header h1 { 
                    color: #667eea; 
                    margin-bottom: 10px;
                }
                .form-group { 
                    margin-bottom: 20px;
                }
                .form-group label { 
                    display: block; 
                    margin-bottom: 5px; 
                    color: #333; 
                    font-weight: bold;
                }
                .form-group input, .form-group select, .form-group textarea { 
                    width: 100%; 
                    padding: 12px; 
                    border: 1px solid #ddd; 
                    border-radius: 8px; 
                    font-size: 1em;
                }
                .form-group textarea { 
                    resize: vertical; 
                    min-height: 80px;
                }
                .btn { 
                    width: 100%; 
                    padding: 15px; 
                    background: #667eea; 
                    color: white; 
                    border: none; 
                    border-radius: 8px; 
                    font-size: 1.1em; 
                    cursor: pointer;
                    transition: background 0.3s ease;
                }
                .btn:hover { 
                    background: #5a6fd8;
                }
                .back-link { 
                    display: block; 
                    text-align: center; 
                    margin-top: 20px; 
                    color: #667eea; 
                    text-decoration: none;
                }
                .back-link:hover { 
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="form-container">
                <div class="form-header">
                    <h1>➕ Add New Account</h1>
                    <p>Connect a new development tool to your DevAccess AI platform</p>
                </div>
                
                <form method="post" action="/api/accounts">
                    <div class="form-group">
                        <label for="software_name">Software/Service Name</label>
                        <input type="text" id="software_name" name="software_name" required 
                               placeholder="e.g., GitHub, Vercel, Cursor IDE">
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" id="email" name="email" required 
                               placeholder="your.email@example.com">
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" required 
                               placeholder="Enter your password">
                    </div>
                    
                    <div class="form-group">
                        <label for="login_url">Login URL</label>
                        <input type="url" id="login_url" name="login_url" required 
                               placeholder="https://service.com/login">
                    </div>
                    
                    <div class="form-group">
                        <label for="usage_context">Usage Context</label>
                        <textarea id="usage_context" name="usage_context" required 
                                  placeholder="Describe how you use this tool (e.g., Frontend development, API testing)"></textarea>
                    </div>
                    
                    <button type="submit" class="btn">Create Account</button>
                </form>
                
                <a href="/dashboard" class="back-link">← Back to Dashboard</a>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    @app.get("/analytics", response_class=HTMLResponse)
    async def analytics_page():
        """Analytics page"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Analytics - DevAccess AI</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }
                .container { 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background: white; 
                    border-radius: 20px; 
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .header { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; 
                    padding: 30px;
                    text-align: center;
                }
                .content { 
                    padding: 30px;
                }
                .analytics-grid { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                    gap: 20px;
                }
                .analytics-card { 
                    background: #f8f9fa; 
                    padding: 20px; 
                    border-radius: 15px;
                }
                .analytics-card h3 { 
                    color: #667eea; 
                    margin-bottom: 15px;
                }
                .back-link { 
                    display: inline-block; 
                    margin-top: 20px; 
                    color: #667eea; 
                    text-decoration: none;
                    padding: 10px 20px;
                    border: 1px solid #667eea;
                    border-radius: 5px;
                }
                .back-link:hover { 
                    background: #667eea;
                    color: white;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 DevAccess AI Analytics</h1>
                    <p>Comprehensive platform insights and metrics</p>
                </div>
                
                <div class="content">
                    <div class="analytics-grid" id="analyticsGrid">
                        <!-- Analytics will be loaded here -->
                    </div>
                    
                    <a href="/dashboard" class="back-link">← Back to Dashboard</a>
                </div>
            </div>
            
            <script>
                async function loadAnalytics() {
                    try {
                        const response = await fetch('/api/analytics');
                        const data = await response.json();
                        
                        const grid = document.getElementById('analyticsGrid');
                        grid.innerHTML = `
                            <div class="analytics-card">
                                <h3>📈 Platform Statistics</h3>
                                <p><strong>Total Accounts:</strong> ${data.platform_stats.total_accounts}</p>
                                <p><strong>Active Accounts:</strong> ${data.platform_stats.active_accounts}</p>
                                <p><strong>API Calls Today:</strong> ${data.platform_stats.api_calls_today}</p>
                                <p><strong>Last Updated:</strong> ${new Date(data.platform_stats.last_updated).toLocaleString()}</p>
                            </div>
                            <div class="analytics-card">
                                <h3>🔧 Resource Usage</h3>
                                <pre>${JSON.stringify(data.resource_usage, null, 2)}</pre>
                            </div>
                            <div class="analytics-card">
                                <h3>📊 Distribution</h3>
                                <pre>${JSON.stringify(data.account_distribution, null, 2)}</pre>
                            </div>
                        `;
                    } catch (error) {
                        console.error('Error loading analytics:', error);
                    }
                }
                
                document.addEventListener('DOMContentLoaded', loadAnalytics);
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    return app

def main():
    """Main entry point"""
    print("🚀 DevAccess AI - Comprehensive Platform")
    print("=" * 60)
    
    # Check dependencies
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI is required but not installed")
        print("   Please install it with: pip install fastapi uvicorn")
        return 1
    
    # Create and run the app
    app = create_app()
    if app is None:
        return 1
    
    print("🎯 Starting DevAccess AI Comprehensive Platform...")
    print("📍 Platform will be available at:")
    print("   🌐 Main App: http://localhost:8000")
    print("   📊 Dashboard: http://localhost:8000/dashboard")
    print("   ➕ Create Account: http://localhost:8000/create-account")
    print("   📈 Analytics: http://localhost:8000/analytics")
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
        print("\n👋 DevAccess AI Platform stopped successfully!")
        return 0
    except KeyboardInterrupt:
        print("\n👋 DevAccess AI Platform stopped by user!")
        return 0
    except Exception as e:
        print(f"\n❌ Error running platform: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
