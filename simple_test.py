#!/usr/bin/env python3
"""
Simple test script to verify AlgoTradeHub is working
"""

import requests
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def test_backend():
    """Test if backend is running and responding"""
    try:
        console.print("🔍 Testing Backend API...", style="bold blue")
        
        # Test basic health check
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            console.print("✅ Backend health check: OK", style="green")
        else:
            console.print(f"❌ Backend health check failed: {response.status_code}", style="red")
            return False
        
        # Test status endpoint
        response = requests.get("http://localhost:5000/api/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            console.print("✅ Backend status API: OK", style="green")
            
            # Display status info
            table = Table(title="Backend Status")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Status", status.get('status', 'unknown'))
            table.add_row("Scanner Running", str(status.get('scanner_running', False)))
            table.add_row("Active Exchanges", str(status.get('active_exchanges', 0)))
            table.add_row("Total Trades", str(status.get('total_trades', 0)))
            
            console.print(table)
        else:
            console.print(f"❌ Backend status API failed: {response.status_code}", style="red")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        console.print("❌ Cannot connect to backend. Is it running on http://localhost:5000?", style="red")
        return False
    except Exception as e:
        console.print(f"❌ Backend test error: {e}", style="red")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    try:
        console.print("🔍 Testing Frontend...", style="bold blue")
        
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            console.print("✅ Frontend accessible: OK", style="green")
            return True
        else:
            console.print(f"❌ Frontend not accessible: {response.status_code}", style="red")
            return False
            
    except requests.exceptions.ConnectionError:
        console.print("❌ Cannot connect to frontend. Is it running on http://localhost:3000?", style="red")
        return False
    except Exception as e:
        console.print(f"❌ Frontend test error: {e}", style="red")
        return False

def main():
    """Main test function"""
    console.print(Panel.fit("🧪 AlgoTradeHub System Test", style="bold magenta"))
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    console.print("\n" + "="*50)
    if backend_ok and frontend_ok:
        console.print("🎉 All systems operational!", style="bold green")
        console.print("🌐 Frontend: http://localhost:3000", style="cyan")
        console.print("🔧 Backend: http://localhost:5000", style="cyan")
    elif backend_ok:
        console.print("⚠️  Backend OK, Frontend needs attention", style="yellow")
        console.print("🔧 Backend: http://localhost:5000", style="cyan")
        console.print("❌ Frontend: Not accessible", style="red")
    else:
        console.print("❌ System issues detected", style="red")
        console.print("Please check if services are running")

if __name__ == "__main__":
    main()