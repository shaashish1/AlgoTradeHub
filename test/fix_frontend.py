#!/usr/bin/env python3
"""
Frontend Fix Script
Automatically fixes and sets up the AlgoTradeHub frontend
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

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
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*50}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{title.center(50)}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*50}{Colors.END}")

def check_node_npm():
    """Check if Node.js and npm are available"""
    print_header("CHECKING NODE.JS & NPM")
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"Node.js found: {version}")
            
            # Check version
            version_num = int(version.replace('v', '').split('.')[0])
            if version_num >= 18:
                print_success("Node.js version is adequate (18+)")
            else:
                print_warning(f"Node.js version {version} might be too old (recommend 18+)")
        else:
            print_error("Node.js not found")
            return False
    except Exception as e:
        print_error(f"Node.js check failed: {e}")
        print_info("Please install Node.js from https://nodejs.org/")
        return False
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"npm found: {version}")
            return True
        else:
            print_error("npm not found")
            return False
    except Exception as e:
        print_error(f"npm check failed: {e}")
        return False

def clean_frontend():
    """Clean previous installation"""
    print_header("CLEANING PREVIOUS INSTALLATION")
    
    frontend_dir = Path('frontend')
    if not frontend_dir.exists():
        print_error("Frontend directory not found!")
        return False
    
    os.chdir(frontend_dir)
    
    # Remove node_modules
    if Path('node_modules').exists():
        print_info("Removing old node_modules...")
        try:
            shutil.rmtree('node_modules')
            print_success("node_modules removed")
        except Exception as e:
            print_warning(f"Could not remove node_modules: {e}")
    
    # Remove package-lock.json
    if Path('package-lock.json').exists():
        print_info("Removing old package-lock.json...")
        try:
            os.remove('package-lock.json')
            print_success("package-lock.json removed")
        except Exception as e:
            print_warning(f"Could not remove package-lock.json: {e}")
    
    return True

def install_dependencies():
    """Install npm dependencies"""
    print_header("INSTALLING DEPENDENCIES")
    
    print_info("Running 'npm install'...")
    print_info("This may take a few minutes...")
    
    try:
        # First try normal install
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print_success("Dependencies installed successfully!")
            return True
        else:
            print_warning("npm install failed, trying with --legacy-peer-deps...")
            
            # Try with legacy peer deps
            result = subprocess.run(['npm', 'install', '--legacy-peer-deps'], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print_success("Dependencies installed with --legacy-peer-deps!")
                return True
            else:
                print_error("npm install failed even with --legacy-peer-deps")
                print("Error output:")
                print(result.stderr)
                return False
                
    except subprocess.TimeoutExpired:
        print_error("npm install timed out (took more than 5 minutes)")
        return False
    except Exception as e:
        print_error(f"npm install failed: {e}")
        return False

def test_build():
    """Test if the project can build"""
    print_header("TESTING BUILD")
    
    try:
        print_info("Running 'npm run build'...")
        result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print_success("Build test successful!")
            return True
        else:
            print_warning("Build test failed")
            print("Build output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Build test timed out")
        return False
    except Exception as e:
        print_error(f"Build test failed: {e}")
        return False

def verify_installation():
    """Verify the installation is working"""
    print_header("VERIFYING INSTALLATION")
    
    # Check if node_modules exists
    if Path('node_modules').exists():
        print_success("node_modules directory exists")
    else:
        print_error("node_modules directory missing")
        return False
    
    # Check key dependencies
    key_deps = ['next', 'react', 'tailwindcss', 'typescript']
    for dep in key_deps:
        dep_path = Path('node_modules') / dep
        if dep_path.exists():
            print_success(f"Dependency verified: {dep}")
        else:
            print_error(f"Dependency missing: {dep}")
            return False
    
    return True

def create_env_file():
    """Create .env.local file if it doesn't exist"""
    print_header("CREATING ENVIRONMENT FILE")
    
    env_file = Path('.env.local')
    if not env_file.exists():
        env_content = """# AlgoTradeHub Frontend Environment
NEXT_PUBLIC_APP_NAME=AlgoTradeHub
NEXT_PUBLIC_API_URL=http://localhost:5000
"""
        try:
            with open(env_file, 'w') as f:
                f.write(env_content)
            print_success("Created .env.local file")
        except Exception as e:
            print_warning(f"Could not create .env.local: {e}")
    else:
        print_info(".env.local already exists")

def start_dev_server():
    """Start the development server"""
    print_header("STARTING DEVELOPMENT SERVER")
    
    print_info("Starting Next.js development server...")
    print_info("The server will be available at: http://localhost:3000")
    print_info("Press Ctrl+C to stop the server")
    print_info("Starting in 3 seconds...")
    
    import time
    time.sleep(3)
    
    try:
        subprocess.run(['npm', 'run', 'dev'])
    except KeyboardInterrupt:
        print_info("\nDevelopment server stopped by user")
    except Exception as e:
        print_error(f"Failed to start development server: {e}")

def main():
    """Main function"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("🚀 ALGOTRADEHUB FRONTEND FIX")
    print("=" * 50)
    print(f"{Colors.END}")
    
    original_dir = os.getcwd()
    
    try:
        # Step 1: Check Node.js and npm
        if not check_node_npm():
            return False
        
        # Step 2: Clean previous installation
        if not clean_frontend():
            return False
        
        # Step 3: Install dependencies
        if not install_dependencies():
            return False
        
        # Step 4: Verify installation
        if not verify_installation():
            return False
        
        # Step 5: Create environment file
        create_env_file()
        
        # Step 6: Test build
        build_success = test_build()
        
        print_header("FRONTEND FIX COMPLETE")
        
        if build_success:
            print_success("✅ Frontend is fully working!")
        else:
            print_warning("⚠️ Frontend installed but build test failed")
            print_info("You can still try running the development server")
        
        print_info("Frontend setup completed successfully!")
        print_info("You can now run:")
        print_info("  cd frontend")
        print_info("  npm run dev")
        print_info("Then visit: http://localhost:3000")
        
        # Ask if user wants to start dev server
        try:
            response = input(f"\n{Colors.YELLOW}Start development server now? (y/n): {Colors.END}")
            if response.lower() in ['y', 'yes']:
                start_dev_server()
        except KeyboardInterrupt:
            print_info("\nSkipping development server start")
        
        return True
        
    except Exception as e:
        print_error(f"Frontend fix failed: {e}")
        return False
    finally:
        # Return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Frontend fix completed successfully!{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ Frontend fix failed{Colors.END}")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Frontend fix interrupted by user{Colors.END}")
        sys.exit(1)