#!/usr/bin/env python3
"""
AlgoTradeHub System Status Checker
Quick overview of system status and next steps
"""

import subprocess
import sys
import os
import importlib
from datetime import datetime

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

def check_component(name, check_func):
    """Check a component and return status"""
    try:
        result = check_func()
        if result:
            print_success(f"{name}")
            return True
        else:
            print_error(f"{name}")
            return False
    except Exception as e:
        print_error(f"{name} - Error: {e}")
        return False

def check_python():
    """Check Python version"""
    version = sys.version_info
    return version >= (3, 8)

def check_nodejs():
    """Check Node.js installation"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def check_npm():
    """Check npm installation"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def check_core_packages():
    """Check core Python packages"""
    packages = ['pandas', 'numpy', 'ccxt', 'ta', 'flask', 'rich']
    for package in packages:
        try:
            importlib.import_module(package)
        except ImportError:
            return False
    return True

def check_crypto_module():
    """Check crypto module"""
    try:
        import crypto
        return True
    except:
        return False

def check_data_acquisition():
    """Check data acquisition functionality"""
    try:
        from crypto.data_acquisition import get_health_status
        health = get_health_status()
        return health.get('status') == 'healthy'
    except:
        return False

def check_frontend_files():
    """Check frontend files exist"""
    required_files = [
        'frontend/package.json',
        'frontend/app/page.tsx',
        'frontend/app/layout.tsx'
    ]
    return all(os.path.exists(f) for f in required_files)

def check_frontend_deps():
    """Check frontend dependencies"""
    return os.path.exists('frontend/node_modules')

def check_main_files():
    """Check main application files"""
    required_files = ['main.py', 'app.py', 'strategy.py', 'backtest.py']
    return all(os.path.exists(f) for f in required_files)

def get_system_info():
    """Get system information"""
    info = {}
    
    # Python version
    info['python_version'] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # Node.js version
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        info['nodejs_version'] = result.stdout.strip() if result.returncode == 0 else "Not installed"
    except:
        info['nodejs_version'] = "Not installed"
    
    # npm version
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
        info['npm_version'] = result.stdout.strip() if result.returncode == 0 else "Not installed"
    except:
        info['npm_version'] = "Not installed"
    
    # Working directory
    info['working_dir'] = os.getcwd()
    
    return info

def main():
    """Main function"""
    print(f"{Colors.MAGENTA}{Colors.BOLD}")
    print("🔍 ALGOTRADEHUB SYSTEM STATUS")
    print("=" * 60)
    print(f"Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.END}")
    
    # Get system info
    info = get_system_info()
    
    print_header("SYSTEM INFORMATION")
    print_info(f"Python Version: {info['python_version']}")
    print_info(f"Node.js Version: {info['nodejs_version']}")
    print_info(f"npm Version: {info['npm_version']}")
    print_info(f"Working Directory: {info['working_dir']}")
    
    print_header("COMPONENT STATUS")
    
    # Check all components
    components = [
        ("Python 3.8+", check_python),
        ("Node.js", check_nodejs),
        ("npm", check_npm),
        ("Core Python Packages", check_core_packages),
        ("Crypto Module", check_crypto_module),
        ("Data Acquisition", check_data_acquisition),
        ("Main Application Files", check_main_files),
        ("Frontend Files", check_frontend_files),
        ("Frontend Dependencies", check_frontend_deps),
    ]
    
    results = {}
    for name, check_func in components:
        results[name] = check_component(name, check_func)
    
    # Calculate overall status
    total_components = len(results)
    working_components = sum(results.values())
    
    print_header("OVERALL STATUS")
    
    if working_components == total_components:
        print_success(f"🎉 ALL SYSTEMS READY! ({working_components}/{total_components})")
        status = "READY"
    elif working_components >= total_components * 0.7:
        print_warning(f"⚠️ MOSTLY READY ({working_components}/{total_components})")
        status = "PARTIAL"
    else:
        print_error(f"❌ NEEDS SETUP ({working_components}/{total_components})")
        status = "NEEDS_SETUP"
    
    print_header("WHAT YOU CAN DO NOW")
    
    # Backend options
    if results.get("Python 3.8+") and results.get("Core Python Packages") and results.get("Crypto Module"):
        print_success("Backend is ready!")
        print_info("• Run main application: python main.py")
        print_info("• Run web dashboard: python app.py")
        print_info("• Run batch testing: python crypto/scripts/batch_runner.py --auto")
    else:
        print_warning("Backend needs setup")
        print_info("• Install dependencies: pip install -r requirements.txt")
    
    # Frontend options
    if results.get("Node.js") and results.get("npm") and results.get("Frontend Dependencies"):
        print_success("Frontend is ready!")
        print_info("• Start dev server: cd frontend && npm run dev")
        print_info("• Visit: http://localhost:3000")
    elif results.get("Node.js") and results.get("npm"):
        print_warning("Frontend needs dependency installation")
        print_info("• Setup frontend: python frontend_complete_setup.py")
    else:
        print_warning("Frontend needs Node.js")
        print_info("• Install Node.js: https://nodejs.org/")
        print_info("• Then run: python frontend_complete_setup.py")
    
    print_header("RECOMMENDED NEXT STEPS")
    
    if status == "READY":
        print_info("🚀 Everything is ready! Choose your preferred way to start:")
        print_info("• Quick start guide: python quick_start.py")
        print_info("• Main application: python main.py")
        print_info("• Web dashboard: python app.py")
        print_info("• Frontend: cd frontend && npm run dev")
    
    elif status == "PARTIAL":
        print_info("🔧 Fix the remaining issues:")
        
        if not results.get("Node.js"):
            print_info("1. Install Node.js from https://nodejs.org/")
        
        if not results.get("Frontend Dependencies"):
            print_info("2. Setup frontend: python frontend_complete_setup.py")
        
        if not results.get("Core Python Packages"):
            print_info("3. Install Python packages: pip install -r requirements.txt")
        
        print_info("4. Run this check again: python system_status.py")
    
    else:
        print_info("🛠️ Complete setup required:")
        print_info("1. Run comprehensive setup: python quick_start.py")
        print_info("2. Or follow manual setup in README.md")
    
    print_header("TESTING & TROUBLESHOOTING")
    print_info("• Full system test: python test_all_systems.py")
    print_info("• Frontend fix: python fix_frontend.py")
    print_info("• Node.js check: python check_nodejs.py")
    
    print(f"\n{Colors.CYAN}Status check completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    
    return status == "READY"

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Status check interrupted{Colors.END}")
        sys.exit(1)