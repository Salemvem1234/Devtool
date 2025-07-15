#!/usr/bin/env python3
"""
DevAccess AI - Startup Script
Quick launcher for the integrated platform
"""
import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import sqlalchemy
        import structlog
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    """Main startup function"""
    print("🚀 DevAccess AI - Integrated Platform Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run this script from the DevAccess AI directory.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n🔧 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
    
    print("\n🎯 Starting DevAccess AI Platform...")
    print("📍 Platform will be available at:")
    print("   🌐 Frontend: http://localhost:8000")
    print("   📊 Dashboard: http://localhost:8000/dashboard") 
    print("   ➕ Create Account: http://localhost:8000/create-account")
    print("   🔧 API Docs: http://localhost:8000/api/docs")
    print("   💚 Health Check: http://localhost:8000/api/health")
    print("\n⚡ Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the application
        import uvicorn
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 DevAccess AI Platform stopped. Thanks for using DevAccess AI!")
    except Exception as e:
        print(f"\n❌ Error starting the platform: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
