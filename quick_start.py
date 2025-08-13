#!/usr/bin/env python3
"""
AlgoTradeHub Quick Start Script
One-click setup and launch for the entire system
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

# Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_header(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{title.center(60)}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")

def print_banner():
    """Print the welcome banner"""
    banner = f"""
{Colors.MAGENTA}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🚀 AlgoTradeHub 🚀                        ║
║                     Quick Start Guide                        ║
║                                                              ║
║  Get your complete trading platform running in minutes!     ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def check_python():
    """Check Python installation"""
    print_header("CHECKING PYTHON")
    
    version = sys.version_info
    if version >= (3, 8):
        print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} is too old (need 3.8+)")
        return False

def check_nodejs():
    """Check Node.js installation"""
    print_header("CHECKING NODE.JS")
    
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"Node.js {version} ✓")
            
            # Check npm
            npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=10)
            if npm_result.returncode == 0:
                npm_version = npm_result.stdout.strip()
                print_success(f"npm {npm_version} ✓")
                return True
            else:
                print_error("npm not found")
                return False
        else:
            print_error("Node.js not found")
            return False
    except Exception:
        print_error("Node.js not installed")
        return False

def check_dependencies():
    """Check Python dependencies"""
    print_header("CHECKING PYTHON DEPENDENCIES")
    
    required_packages = ['pandas', 'numpy', 'ccxt', 'ta', 'matplotlib', 'plotly', 'flask', 'rich']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} ✓")
        except ImportError:
            print_error(f"{package} ❌")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"Missing packages: {', '.join(missing_packages)}")
        print_info("Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def test_backend():
    """Test backend functionality"""
    print_header("TESTING BACKEND")
    
    try:
        # Test crypto module
        import crypto
        print_success("Crypto module ✓")
        
        # Test data acquisition
        from crypto.data_acquisition import get_health_status
        health = get_health_status()
        if health.get('status') == 'healthy':
            print_success("Data acquisition ✓")
            working_exchanges = health.get('working_exchanges', [])
            print_info(f"Working exchanges: {', '.join(working_exchanges)}")
        else:
            print_warning("Data acquisition has issues (might be network)")
        
        return True
    except Exception as e:
        print_error(f"Backend test failed: {e}")
        return False

def setup_frontend():
    """Set up frontend if Node.js is available"""
    print_header("SETTING UP FRONTEND")
    
    if not os.path.exists('frontend'):
        print_error("Frontend directory not found")
        return False
    
    original_dir = os.getcwd()
    
    try:
        os.chdir('frontend')
        
        # Check if already set up
        if os.path.exists('node_modules') and os.path.exists('node_modules/next'):
            print_success("Frontend already set up ✓")
            return True
        
        print_info("Installing frontend dependencies...")
        
        # Install dependencies
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print_warning("Trying with --legacy-peer-deps...")
            result = subprocess.run(['npm', 'install', '--legacy-peer-deps'], 
                                  capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print_success("Frontend dependencies installed ✓")
            return True
        else:
            print_error("Frontend setup failed")
            return False
            
    except Exception as e:
        print_error(f"Frontend setup error: {e}")
        return False
    finally:
        os.chdir(original_dir)

def provide_launch_options(backend_ok, frontend_ok):
    """Provide launch options based on what's working"""
    print_header("LAUNCH OPTIONS")
    
    options = []
    
    if backend_ok:
        options.extend([
            ("1", "🐍 Python Backend - Main Application", "python main.py"),
            ("2", "🌐 Web Dashboard", "python app.py"),
            ("3", "📊 Batch Runner (Crypto Scripts)", "python crypto/scripts/batch_runner.py --help"),
            ("4", "🧪 Run All Tests", "python test_all_systems.py")
        ])
    
    if frontend_ok:
        options.extend([
            ("5", "⚛️ Frontend Development Server", "cd frontend && npm run dev"),
            ("6", "🚀 Full Stack (Backend + Frontend)", "Launch both simultaneously")
        ])
    
    if not backend_ok and not frontend_ok:
        print_error("Neither backend nor frontend is ready")
        return None
    
    # Display options
    for num, desc, cmd in options:
        print_info(f"{num}. {desc}")
        if not cmd.startswith("Launch"):
            print(f"   Command: {Colors.CYAN}{cmd}{Colors.END}")
    
    print_info("0. Exit")
    
    return options

def launch_application(choice, options):
    """Launch the selected application"""
    try:
        choice_num = int(choice)
        
        if choice_num == 0:
            print_info("Goodbye!")
            return
        
        if choice_num == 6:  # Full stack
            print_header("LAUNCHING FULL STACK")
            print_info("Starting backend and frontend...")
            
            # Start backend in background
            print_info("Starting backend (python app.py)...")
            backend_process = subprocess.Popen(['python', 'app.py'])
            
            time.sleep(3)  # Give backend time to start
            
            # Start frontend
            print_info("Starting frontend...")
            os.chdir('frontend')
            
            print_info("Backend: http://localhost:5000")
            print_info("Frontend: http://localhost:3000")
            print_info("Press Ctrl+C to stop both servers")
            
            try:
                subprocess.run(['npm', 'run', 'dev'])
            except KeyboardInterrupt:
                print_info("Stopping servers...")
                backend_process.terminate()
            
            return
        
        # Find the selected option
        selected_option = None
        for num, desc, cmd in options:
            if num == str(choice_num):
                selected_option = (desc, cmd)
                break
        
        if selected_option:
            desc, cmd = selected_option
            print_header(f"LAUNCHING: {desc}")
            print_info(f"Command: {cmd}")
            
            if cmd.startswith("cd frontend"):
                os.chdir('frontend')
                subprocess.run(['npm', 'run', 'dev'])
            else:
                subprocess.run(cmd.split())
        else:
            print_error("Invalid choice")
            
    except ValueError:
        print_error("Please enter a valid number")
    except KeyboardInterrupt:
        print_info("Launch cancelled")
    except Exception as e:
        print_error(f"Launch failed: {e}")

def main():
    """Main function"""
    print_banner()
    
    # System checks
    python_ok = check_python()
    nodejs_ok = check_nodejs()
    deps_ok = check_dependencies() if python_ok else False
    backend_ok = test_backend() if deps_ok else False
    frontend_ok = setup_frontend() if nodejs_ok else False
    
    # Summary
    print_header("SYSTEM STATUS")
    
    status_items = [
        ("Python", python_ok),
        ("Node.js", nodejs_ok),
        ("Python Dependencies", deps_ok),
        ("Backend", backend_ok),
        ("Frontend", frontend_ok)
    ]
    
    for item, status in status_items:
        if status:
            print_success(f"{item} ✓")
        else:
            print_error(f"{item} ❌")
    
    # Provide guidance based on status
    if not python_ok:
        print_error("Python 3.8+ is required")
        return False
    
    if not nodejs_ok:
        print_warning("Node.js not found - frontend will not work")
        print_info("Install Node.js from: https://nodejs.org/")
        
        try:
            response = input(f"{Colors.YELLOW}Open Node.js website? (y/n): {Colors.END}")
            if response.lower() in ['y', 'yes']:
                webbrowser.open('https://nodejs.org/')
        except KeyboardInterrupt:
            pass
    
    if not deps_ok:
        print_warning("Some Python dependencies are missing")
        print_info("Run: pip install -r requirements.txt")
    
    # Launch options
    if backend_ok or frontend_ok:
        options = provide_launch_options(backend_ok, frontend_ok)
        
        if options:
            try:
                choice = input(f"\n{Colors.YELLOW}Select option (0-{len(options)}): {Colors.END}")
                launch_application(choice, options)
            except KeyboardInterrupt:
                print_info("Goodbye!")
    else:
        print_header("NEXT STEPS")
        print_info("To get started:")
        
        if not nodejs_ok:
            print_info("1. Install Node.js from https://nodejs.org/")
        
        if not deps_ok:
            print_info("2. Install Python dependencies: pip install -r requirements.txt")
        
        print_info("3. Run this script again: python quick_start.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Quick start interrupted{Colors.END}")
        sys.exit(1)