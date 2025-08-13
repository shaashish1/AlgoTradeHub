#!/usr/bin/env python3
"""
AlgoTrading Application Startup Script
Starts both the Flask backend and Next.js frontend
"""

import subprocess
import sys
import os
import time
import threading
import signal
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        import pandas
        import numpy
        print("✅ Python dependencies found")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        print("Please install Node.js from https://nodejs.org/")
        return False
    
    # Check if frontend dependencies are installed
    frontend_path = Path("frontend")
    if not (frontend_path / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], cwd=frontend_path, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return False
    else:
        print("✅ Frontend dependencies found")
    
    return True

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Flask backend server...")
    try:
        # Set environment variables
        env = os.environ.copy()
        env['FLASK_ENV'] = 'development'
        env['FLASK_DEBUG'] = 'true'
        
        # Start Flask app
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print backend output
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[Backend] {line.rstrip()}")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the Next.js frontend server"""
    print("🚀 Starting Next.js frontend server...")
    try:
        frontend_path = Path("frontend")
        
        # Start Next.js dev server
        process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd=frontend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print frontend output
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[Frontend] {line.rstrip()}")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutting down application...")
    sys.exit(0)

def main():
    """Main startup function"""
    print("🎯 AlgoTrading Application Startup")
    print("=" * 50)
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please resolve the issues above.")
        sys.exit(1)
    
    print("\n🚀 Starting application servers...")
    print("=" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend in a separate thread
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    
    # Wait a moment for frontend to start
    time.sleep(5)
    
    print("\n✅ Application started successfully!")
    print("=" * 50)
    print("🌐 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:5000")
    print("📊 Backend Dashboard: http://localhost:5000")
    print("=" * 50)
    print("Press Ctrl+C to stop the application")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()