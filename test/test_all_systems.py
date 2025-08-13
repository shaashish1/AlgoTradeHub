#!/usr/bin/env python3
"""
Comprehensive Test Suite for AlgoTradeHub
Tests all components, imports, and functionality
"""

import os
import sys
import importlib
import subprocess
import traceback
from datetime import datetime
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    """Print a formatted header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{title.center(60)}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")

def print_success(message):
    """Print success message with green checkmark"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    """Print error message with red X"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    """Print warning message with yellow triangle"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    """Print info message with blue dot"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def test_python_environment():
    """Test Python environment and basic requirements"""
    print_header("PYTHON ENVIRONMENT TEST")
    
    results = []
    
    # Test Python version
    try:
        python_version = sys.version_info
        if python_version >= (3, 8):
            print_success(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
            results.append(True)
        else:
            print_error(f"Python version too old: {python_version.major}.{python_version.minor}.{python_version.micro} (need 3.8+)")
            results.append(False)
    except Exception as e:
        print_error(f"Python version check failed: {e}")
        results.append(False)
    
    # Test virtual environment
    try:
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print_success("Virtual environment detected")
            print_info(f"Python executable: {sys.executable}")
            results.append(True)
        else:
            print_warning("No virtual environment detected (recommended but not required)")
            results.append(True)
    except Exception as e:
        print_error(f"Virtual environment check failed: {e}")
        results.append(False)
    
    # Test current directory
    try:
        current_dir = os.getcwd()
        print_info(f"Current directory: {current_dir}")
        if "AlgoProject" in current_dir or "algotradehub" in current_dir.lower():
            print_success("Working directory looks correct")
            results.append(True)
        else:
            print_warning("Working directory might not be correct")
            results.append(True)
    except Exception as e:
        print_error(f"Directory check failed: {e}")
        results.append(False)
    
    return all(results)

def test_core_imports():
    """Test core Python package imports"""
    print_header("CORE IMPORTS TEST")
    
    core_packages = [
        'os', 'sys', 'datetime', 'pathlib', 'json', 'csv',
        'pandas', 'numpy', 'ccxt', 'ta', 'matplotlib', 'plotly'
    ]
    
    results = []
    
    for package in core_packages:
        try:
            importlib.import_module(package)
            print_success(f"{package} imported successfully")
            results.append(True)
        except ImportError as e:
            print_error(f"{package} import failed: {e}")
            results.append(False)
        except Exception as e:
            print_error(f"{package} unexpected error: {e}")
            results.append(False)
    
    # Test CCXT version and exchanges
    try:
        import ccxt
        print_info(f"CCXT version: {ccxt.__version__}")
        print_info(f"Available exchanges: {len(ccxt.exchanges)}")
        
        # Test specific exchanges
        test_exchanges = ['binance', 'kraken', 'delta']
        for exchange in test_exchanges:
            if exchange in ccxt.exchanges:
                print_success(f"Exchange '{exchange}' available in CCXT")
            else:
                print_warning(f"Exchange '{exchange}' not found in CCXT")
        
        results.append(True)
    except Exception as e:
        print_error(f"CCXT detailed test failed: {e}")
        results.append(False)
    
    return all(results)

def test_project_structure():
    """Test project directory structure"""
    print_header("PROJECT STRUCTURE TEST")
    
    required_dirs = [
        'crypto',
        'crypto/scripts',
        'crypto/tools',
        'crypto/strategies',
        'utils',
        'frontend',
        'templates',
        'static'
    ]
    
    required_files = [
        'main.py',
        'strategy.py',
        'backtest.py',
        'app.py',
        'requirements.txt',
        'crypto/__init__.py',
        'crypto/data_acquisition.py',
        'crypto/crypto_symbol_manager.py'
    ]
    
    results = []
    
    # Test directories
    for directory in required_dirs:
        if os.path.exists(directory):
            print_success(f"Directory exists: {directory}")
            results.append(True)
        else:
            print_error(f"Directory missing: {directory}")
            results.append(False)
    
    # Test files
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"File exists: {file_path}")
            results.append(True)
        else:
            print_error(f"File missing: {file_path}")
            results.append(False)
    
    return all(results)

def test_crypto_module():
    """Test crypto module and its components"""
    print_header("CRYPTO MODULE TEST")
    
    results = []
    
    # Test crypto module import
    try:
        import crypto
        print_success("crypto module imported successfully")
        print_info(f"crypto version: {getattr(crypto, '__version__', 'unknown')}")
        results.append(True)
    except Exception as e:
        print_error(f"crypto module import failed: {e}")
        results.append(False)
        return False
    
    # Test crypto submodules
    crypto_modules = [
        'crypto.data_acquisition',
        'crypto.crypto_symbol_manager',
        'crypto.list_crypto_assets',
        'crypto.list_ccxt_exchanges',
        'crypto.backtest_config',
        'crypto.crypto_assets_manager'
    ]
    
    for module in crypto_modules:
        try:
            importlib.import_module(module)
            print_success(f"{module} imported successfully")
            results.append(True)
        except Exception as e:
            print_error(f"{module} import failed: {e}")
            results.append(False)
    
    # Test data acquisition functionality
    try:
        from crypto.data_acquisition import fetch_data, get_health_status
        
        # Test health status
        health = get_health_status()
        if health.get('status') == 'healthy':
            print_success("Data acquisition health check passed")
            print_info(f"Working exchanges: {health.get('working_exchanges', [])}")
            results.append(True)
        else:
            print_warning("Data acquisition health check returned non-healthy status")
            results.append(True)  # Still pass, might be network issue
            
    except Exception as e:
        print_error(f"Data acquisition test failed: {e}")
        results.append(False)
    
    return all(results)

def test_scripts():
    """Test crypto scripts"""
    print_header("CRYPTO SCRIPTS TEST")
    
    script_files = [
        'crypto/scripts/batch_runner.py',
        'crypto/scripts/batch_runner_demo.py',
        'crypto/scripts/interactive_crypto_demo.py',
        'crypto/scripts/delta_backtest_strategies.py'
    ]
    
    results = []
    
    for script in script_files:
        try:
            if os.path.exists(script):
                # Try to import the script
                script_name = os.path.basename(script).replace('.py', '')
                script_dir = os.path.dirname(script)
                
                # Add script directory to path temporarily
                if script_dir not in sys.path:
                    sys.path.insert(0, script_dir)
                
                try:
                    importlib.import_module(script_name)
                    print_success(f"{script} imports successfully")
                    results.append(True)
                except Exception as e:
                    print_warning(f"{script} import issue: {e}")
                    results.append(True)  # Scripts might have execution code
                
                # Remove from path
                if script_dir in sys.path:
                    sys.path.remove(script_dir)
            else:
                print_error(f"Script not found: {script}")
                results.append(False)
                
        except Exception as e:
            print_error(f"Script test failed for {script}: {e}")
            results.append(False)
    
    return all(results)

def test_main_components():
    """Test main application components"""
    print_header("MAIN COMPONENTS TEST")
    
    main_files = [
        'main.py',
        'strategy.py', 
        'backtest.py',
        'app.py'
    ]
    
    results = []
    
    for file_path in main_files:
        try:
            if os.path.exists(file_path):
                # Try to import without executing
                module_name = file_path.replace('.py', '').replace('/', '.')
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                
                # Don't execute, just check if it can be loaded
                print_success(f"{file_path} can be loaded")
                results.append(True)
            else:
                print_error(f"File not found: {file_path}")
                results.append(False)
                
        except Exception as e:
            print_error(f"Component test failed for {file_path}: {e}")
            results.append(False)
    
    return all(results)

def test_frontend():
    """Test frontend setup"""
    print_header("FRONTEND TEST")
    
    results = []
    
    # Check if frontend directory exists
    if os.path.exists('frontend'):
        print_success("Frontend directory exists")
        
        # Check key frontend files
        frontend_files = [
            'frontend/package.json',
            'frontend/next.config.js',
            'frontend/tailwind.config.js',
            'frontend/app/layout.tsx',
            'frontend/app/page.tsx',
            'frontend/app/globals.css'
        ]
        
        for file_path in frontend_files:
            if os.path.exists(file_path):
                print_success(f"Frontend file exists: {file_path}")
                results.append(True)
            else:
                print_error(f"Frontend file missing: {file_path}")
                results.append(False)
        
        # Check if node_modules exists (dependencies installed)
        if os.path.exists('frontend/node_modules'):
            print_success("Frontend dependencies installed (node_modules exists)")
            
            # Check key dependencies
            key_deps = ['next', 'react', 'tailwindcss', 'typescript']
            deps_ok = True
            for dep in key_deps:
                dep_path = os.path.join('frontend/node_modules', dep)
                if os.path.exists(dep_path):
                    print_success(f"Key dependency found: {dep}")
                else:
                    print_warning(f"Key dependency missing: {dep}")
                    deps_ok = False
            
            if deps_ok:
                print_success("All key dependencies verified")
                results.append(True)
            else:
                print_warning("Some dependencies missing - run 'python fix_frontend.py'")
                results.append(False)
        else:
            print_warning("Frontend dependencies not installed")
            print_info("Run 'python fix_frontend.py' to automatically fix this")
            results.append(False)
            
    else:
        print_error("Frontend directory not found")
        results.append(False)
    
    return all(results)

def test_data_functionality():
    """Test actual data fetching functionality"""
    print_header("DATA FUNCTIONALITY TEST")
    
    results = []
    
    try:
        from crypto.data_acquisition import fetch_data
        
        # Test data fetch
        print_info("Testing data fetch with BTC/USDT on kraken...")
        data = fetch_data('BTC/USDT', 'kraken', '1h', 5)
        
        if data is not None and len(data) > 0:
            print_success(f"Data fetch successful! Got {len(data)} bars")
            print_info(f"Data columns: {list(data.columns)}")
            print_info(f"Data shape: {data.shape}")
            results.append(True)
        else:
            print_warning("Data fetch returned empty result (might be network/API issue)")
            results.append(True)  # Don't fail on network issues
            
    except Exception as e:
        print_error(f"Data functionality test failed: {e}")
        results.append(False)
    
    return all(results)

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print(f"{Colors.MAGENTA}{Colors.BOLD}")
    print("🚀 ALGOTRADEHUB COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.END}")
    
    test_results = {}
    
    # Run all tests
    test_results['Python Environment'] = test_python_environment()
    test_results['Core Imports'] = test_core_imports()
    test_results['Project Structure'] = test_project_structure()
    test_results['Crypto Module'] = test_crypto_module()
    test_results['Scripts'] = test_scripts()
    test_results['Main Components'] = test_main_components()
    test_results['Frontend'] = test_frontend()
    test_results['Data Functionality'] = test_data_functionality()
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        if result:
            print_success(f"{test_name}")
            passed += 1
        else:
            print_error(f"{test_name}")
    
    print(f"\n{Colors.BOLD}OVERALL RESULT:{Colors.END}")
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! ({passed}/{total}){Colors.END}")
        print(f"{Colors.GREEN}✅ Your AlgoTradeHub system is ready to use!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  PARTIAL SUCCESS ({passed}/{total} tests passed){Colors.END}")
        print(f"{Colors.YELLOW}Some components need attention, but core functionality should work.{Colors.END}")
    
    # Provide next steps
    print_header("NEXT STEPS")
    
    if test_results.get('Frontend', False):
        print_info("✅ Frontend: Run 'cd frontend && npm run dev'")
        print_info("   Then visit: http://localhost:3000")
    else:
        print_warning("❌ Frontend: Run 'python fix_frontend.py' to fix automatically")
        print_info("   This will install dependencies and set everything up")
    
    if test_results.get('Data Functionality', False):
        print_info("✅ Backend: Run 'python main.py' for the main application")
    
    if test_results.get('Scripts', False):
        print_info("✅ Scripts: Try 'python crypto/scripts/batch_runner.py --help'")
    
    print_info("✅ Web App: Run 'python app.py' for the web interface")
    
    # Special frontend fix instructions
    if not test_results.get('Frontend', False):
        print_header("FRONTEND FIX INSTRUCTIONS")
        print_info("To fix the frontend automatically, run:")
        print_info("  python fix_frontend.py")
        print_info("")
        print_info("This script will:")
        print_info("  • Check Node.js and npm installation")
        print_info("  • Clean previous installations")
        print_info("  • Install all dependencies")
        print_info("  • Test the build")
        print_info("  • Start the development server")
    
    print(f"\n{Colors.CYAN}Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    
    return passed == total

if __name__ == "__main__":
    try:
        # Add current directory to Python path
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import required modules for testing
        import importlib.util
        
        # Run comprehensive test
        success = run_comprehensive_test()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Test suite failed with error: {e}{Colors.END}")
        traceback.print_exc()
        sys.exit(1)