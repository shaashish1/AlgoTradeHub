#!/usr/bin/env python3
"""
Complete Frontend Setup Script
Handles Node.js installation check and complete frontend setup
"""

import subprocess
import sys
import os
import webbrowser
import time

# Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
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

def check_nodejs_installation():
    """Check if Node.js is properly installed"""
    print_header("CHECKING NODE.JS INSTALLATION")
    
    try:
        # Check Node.js
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            node_version = result.stdout.strip()
            version_num = int(node_version.replace('v', '').split('.')[0])
            
            print_success(f"Node.js found: {node_version}")
            
            if version_num >= 18:
                print_success("Node.js version is adequate")
            else:
                print_warning(f"Node.js version {node_version} might be too old (recommend 18+)")
            
            # Check npm
            npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=10)
            if npm_result.returncode == 0:
                npm_version = npm_result.stdout.strip()
                print_success(f"npm found: {npm_version}")
                return True
            else:
                print_error("npm not found")
                return False
        else:
            print_error("Node.js not found")
            return False
            
    except Exception as e:
        print_error(f"Node.js check failed: {e}")
        return False

def provide_installation_instructions():
    """Provide Node.js installation instructions"""
    print_header("NODE.JS INSTALLATION REQUIRED")
    
    print_info("Node.js is required for the frontend to work.")
    print_info("")
    print_info("📥 INSTALLATION OPTIONS:")
    print_info("")
    print_info("Option 1 - Official Website (Recommended):")
    print_info("  1. Visit: https://nodejs.org/")
    print_info("  2. Download LTS version (Long Term Support)")
    print_info("  3. Run the installer")
    print_info("  4. Accept all defaults")
    print_info("  5. Restart your command prompt")
    print_info("")
    print_info("Option 2 - Windows Package Manager:")
    print_info("  • Winget: winget install OpenJS.NodeJS")
    print_info("  • Chocolatey: choco install nodejs")
    print_info("")
    print_info("After installation, restart your terminal and run:")
    print_info("  python frontend_complete_setup.py")
    
    try:
        response = input(f"\n{Colors.YELLOW}Open Node.js website now? (y/n): {Colors.END}")
        if response.lower() in ['y', 'yes']:
            print_info("Opening https://nodejs.org/...")
            webbrowser.open('https://nodejs.org/')
            print_info("After installing Node.js, run this script again!")
    except KeyboardInterrupt:
        print_info("Installation instructions provided above")

def setup_frontend():
    """Set up the frontend after Node.js is confirmed"""
    print_header("SETTING UP FRONTEND")
    
    # Check if frontend directory exists
    if not os.path.exists('frontend'):
        print_error("Frontend directory not found!")
        return False
    
    original_dir = os.getcwd()
    
    try:
        os.chdir('frontend')
        
        # Clean previous installation
        print_info("Cleaning previous installation...")
        if os.path.exists('node_modules'):
            print_info("Removing old node_modules...")
            import shutil
            shutil.rmtree('node_modules', ignore_errors=True)
        
        if os.path.exists('package-lock.json'):
            print_info("Removing old package-lock.json...")
            os.remove('package-lock.json')
        
        # Install dependencies
        print_info("Installing dependencies (this may take a few minutes)...")
        
        # Try normal install first
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print_warning("Normal install failed, trying with --legacy-peer-deps...")
            result = subprocess.run(['npm', 'install', '--legacy-peer-deps'], 
                                  capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print_success("Dependencies installed successfully!")
        else:
            print_error("Failed to install dependencies")
            print("Error output:")
            print(result.stderr)
            return False
        
        # Verify key dependencies
        key_deps = ['next', 'react', 'tailwindcss', 'typescript']
        all_deps_ok = True
        
        for dep in key_deps:
            if os.path.exists(f'node_modules/{dep}'):
                print_success(f"Dependency verified: {dep}")
            else:
                print_error(f"Dependency missing: {dep}")
                all_deps_ok = False
        
        if not all_deps_ok:
            print_warning("Some dependencies are missing, but continuing...")
        
        # Test build
        print_info("Testing build...")
        build_result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True, timeout=120)
        
        if build_result.returncode == 0:
            print_success("Build test successful!")
        else:
            print_warning("Build test failed, but you can still try the dev server")
        
        # Create .env.local if it doesn't exist
        if not os.path.exists('.env.local'):
            env_content = """# AlgoTradeHub Frontend Environment
NEXT_PUBLIC_APP_NAME=AlgoTradeHub
NEXT_PUBLIC_API_URL=http://localhost:5000
"""
            with open('.env.local', 'w') as f:
                f.write(env_content)
            print_success("Created .env.local file")
        
        return True
        
    except Exception as e:
        print_error(f"Frontend setup failed: {e}")
        return False
    finally:
        os.chdir(original_dir)

def start_development_server():
    """Start the development server"""
    print_header("STARTING DEVELOPMENT SERVER")
    
    print_info("Starting Next.js development server...")
    print_info("Server will be available at: http://localhost:3000")
    print_info("Press Ctrl+C to stop the server")
    print_info("")
    print_info("Starting in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    try:
        os.chdir('frontend')
        subprocess.run(['npm', 'run', 'dev'])
    except KeyboardInterrupt:
        print_info("\nDevelopment server stopped by user")
    except Exception as e:
        print_error(f"Failed to start development server: {e}")

def main():
    """Main function"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("🚀 ALGOTRADEHUB COMPLETE FRONTEND SETUP")
    print("=" * 60)
    print(f"{Colors.END}")
    
    # Step 1: Check Node.js installation
    if not check_nodejs_installation():
        provide_installation_instructions()
        return False
    
    # Step 2: Set up frontend
    if not setup_frontend():
        print_error("Frontend setup failed")
        return False
    
    # Step 3: Success message
    print_header("SETUP COMPLETE")
    print_success("🎉 Frontend setup completed successfully!")
    print_info("")
    print_info("You can now:")
    print_info("  1. Start dev server: cd frontend && npm run dev")
    print_info("  2. Visit: http://localhost:3000")
    print_info("  3. Test pages:")
    print_info("     • Dashboard: http://localhost:3000")
    print_info("     • Features: http://localhost:3000/features")
    print_info("     • Backtesting: http://localhost:3000/backtest/comprehensive")
    
    # Ask if user wants to start dev server
    try:
        response = input(f"\n{Colors.YELLOW}Start development server now? (y/n): {Colors.END}")
        if response.lower() in ['y', 'yes']:
            start_development_server()
    except KeyboardInterrupt:
        print_info("You can start the server later with: cd frontend && npm run dev")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Frontend is now ready to use!{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ Please install Node.js first, then run this script again{Colors.END}")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup interrupted by user{Colors.END}")
        sys.exit(1)