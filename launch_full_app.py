#!/usr/bin/env python3
"""
Launch Full AlgoTradeHub Application
Starts both Flask backend and Next.js frontend
"""

import subprocess
import sys
import os
import time
import threading
import signal
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def start_backend():
    """Start Flask backend in background"""
    try:
        console.print("🚀 Starting Flask Backend...", style="bold blue")
        
        # Start Flask app
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Give backend time to start
        time.sleep(3)
        console.print("✅ Backend started at http://localhost:5000", style="green")
        return process
        
    except Exception as e:
        console.print(f"❌ Failed to start backend: {e}", style="red")
        return None

def start_frontend():
    """Start Next.js frontend"""
    try:
        console.print("🚀 Starting Next.js Frontend...", style="bold blue")
        
        frontend_path = Path("frontend")
        if not frontend_path.exists():
            console.print("❌ Frontend directory not found", style="red")
            return None
        
        # Start Next.js dev server
        process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd=frontend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Give frontend time to start
        time.sleep(5)
        console.print("✅ Frontend started at http://localhost:3000", style="green")
        return process
        
    except Exception as e:
        console.print(f"❌ Failed to start frontend: {e}", style="red")
        return None

def main():
    """Main launcher"""
    console.print(Panel.fit("🎯 AlgoTradeHub Full Application Launcher", style="bold magenta"))
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        console.print("❌ Cannot start without backend", style="red")
        return
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Display status
    console.print("\n" + "="*60)
    console.print("🎉 AlgoTradeHub is now running!", style="bold green")
    console.print("="*60)
    console.print("🔧 Backend API: http://localhost:5000", style="cyan")
    if frontend_process:
        console.print("🌐 Frontend UI: http://localhost:3000", style="cyan")
        console.print("\n💡 Open http://localhost:3000 for the best experience!", style="bold yellow")
    else:
        console.print("⚠️  Frontend failed to start, using backend only", style="yellow")
        console.print("🌐 Backend UI: http://localhost:5000", style="cyan")
    
    console.print("="*60)
    console.print("Press Ctrl+C to stop all services", style="dim")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n🛑 Shutting down services...", style="yellow")
        
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        console.print("👋 Goodbye!", style="green")

if __name__ == "__main__":
    main()