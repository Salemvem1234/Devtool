#!/usr/bin/env python3
"""
DevAccess AI - Simple Run Script
Runs the DevAccess AI application using the existing backend structure
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main function to run the DevAccess AI application"""
    print("🚀 Starting DevAccess AI Platform...")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path(".")
    backend_dir = current_dir / "devaccess-ai" / "backend"
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        print(f"   Expected: {backend_dir}")
        print("   Make sure you're running this from the correct directory.")
        return 1
        
    # Change to backend directory
    os.chdir(backend_dir)
    print(f"📂 Changed to backend directory: {backend_dir}")
    
    # Check if virtual environment exists
    venv_dir = backend_dir / "venv"
    if venv_dir.exists():
        print("🔧 Using existing virtual environment...")
        # Use the virtual environment's Python
        if sys.platform == "win32":
            python_exe = venv_dir / "bin" / "python.exe"
        else:
            python_exe = venv_dir / "bin" / "python"
        
        if not python_exe.exists():
            print("❌ Virtual environment Python not found!")
            return 1
    else:
        print("⚠️ No virtual environment found, using system Python")
        python_exe = sys.executable
    
    # Run the application
    print("🎯 Starting the application...")
    print("📍 Platform will be available at:")
    print("   🌐 Frontend: http://localhost:8000")
    print("   📊 API Docs: http://localhost:8000/docs")
    print("   💚 Health Check: http://localhost:8000/health")
    print("=" * 50)
    
    try:
        # Run the main application
        cmd = [str(python_exe), "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running the application: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\n👋 DevAccess AI Platform stopped. Thanks for using DevAccess AI!")
        return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
