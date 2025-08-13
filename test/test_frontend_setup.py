#!/usr/bin/env python3
"""
Frontend Setup Test Script
Tests if the Next.js frontend is properly configured and can start
"""

import os
import sys
import subprocess
import json
import time
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

def test_node_npm():
    """Test if Node.js and npm are installed"""
    print_header("NODE.JS & NPM TEST")
    
    results = []
    
    # Test Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"Node.js installed: {version}")
            
            # Check if version is adequate (should be 18+)
            version_num = int(version.replace('v', '').split('.')[0])
            if version_num >= 18:
                print_success("Node.js version is adequate (18+)")
                results.append(True)
            else:
                print_warning(f"Node.js version {version} might be too old (recommend 18+)")
                results.append(True)  # Still might work
        else:
            print_error("Node.js not found or not working")
            results.append(False)
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print_error(f"Node.js test failed: {e}")
        results.append(False)
    
    # Test npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"npm installed: {version}")
            results.append(True)
        else:
            print_error("npm not found or not working")
            results.append(False)
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print_error(f"npm test failed: {e}")
        results.append(False)
    
    return all(results)

def test_frontend_structure():
    """Test frontend directory structure"""
    print_header("FRONTEND STRUCTURE TEST")
    
    if not os.path.exists('frontend'):
        print_error("Frontend directory not found!")
        return False
    
    os.chdir('frontend')
    
    required_files = [
        'package.json',
        'next.config.js',
        'tailwind.config.js',
        'tsconfig.json',
        'postcss.config.js',
        'app/layout.tsx',
        'app/page.tsx',
        'app/globals.css'
    ]
    
    results = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"File exists: {file_path}")
            results.append(True)
        else:
            print_error(f"File missing: {file_path}")
            results.append(False)
    
    # Test package.json content
    try:
        with open('package.json', 'r') as f:
            package_data = json.load(f)
        
        if 'next' in package_data.get('dependencies', {}):
            print_success("Next.js dependency found in package.json")
            results.append(True)
        else:
            print_error("Next.js dependency missing from package.json")
            results.append(False)
            
        if 'tailwindcss' in package_data.get('devDependencies', {}):
            print_success("Tailwind CSS dependency found")
            results.append(True)
        else:
            print_error("Tailwind CSS dependency missing")
            results.append(False)
            
    except Exception as e:
        print_error(f"Error reading package.json: {e}")
        results.append(False)
    
    return all(results)

def test_dependencies():
    """Test if dependencies are installed"""
    print_header("DEPENDENCIES TEST")
    
    if os.path.exists('node_modules'):
        print_success("node_modules directory exists")
        
        # Check for key dependencies
        key_deps = ['next', 'react', 'tailwindcss', 'typescript']
        results = []
        
        for dep in key_deps:
            dep_path = os.path.join('node_modules', dep)
            if os.path.exists(dep_path):
                print_success(f"Dependency installed: {dep}")
                results.append(True)
            else:
                print_error(f"Dependency missing: {dep}")
                results.append(False)
        
        return all(results)
    else:
        print_warning("node_modules not found - dependencies not installed")
        print_info("Run 'npm install' to install dependencies")
        return False

def install_dependencies():
    """Install npm dependencies"""
    print_header("INSTALLING DEPENDENCIES")
    
    try:
        print_info("Running 'npm install'...")
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print_success("Dependencies installed successfully!")
            return True
        else:
            print_error("npm install failed:")
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
    print_header("BUILD TEST")
    
    try:
        print_info("Testing Next.js build...")
        result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print_success("Build successful!")
            return True
        else:
            print_error("Build failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Build timed out")
        return False
    except Exception as e:
        print_error(f"Build test failed: {e}")
        return False

def start_dev_server():
    """Start the development server"""
    print_header("STARTING DEV SERVER")
    
    print_info("Starting Next.js development server...")
    print_info("This will start the server and you can test it manually")
    print_info("Press Ctrl+C to stop the server")
    print_info("Server should be available at: http://localhost:3000")
    
    try:
        # Start the dev server
        subprocess.run(['npm', 'run', 'dev'], timeout=None)
    except KeyboardInterrupt:
        print_info("Development server stopped by user")
    except Exception as e:
        print_error(f"Failed to start dev server: {e}")

def main():
    """Main test function"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("🚀 FRONTEND SETUP TEST")
    print("=" * 50)
    print(f"{Colors.END}")
    
    original_dir = os.getcwd()
    
    try:
        # Test Node.js and npm
        if not test_node_npm():
            print_error("Node.js/npm not available. Please install Node.js first.")
            return False
        
        # Test frontend structure
        if not test_frontend_structure():
            print_error("Frontend structure test failed")
            return False
        
        # Test dependencies
        deps_installed = test_dependencies()
        
        if not deps_installed:
            print_info("Attempting to install dependencies...")
            if not install_dependencies():
                print_error("Failed to install dependencies")
                return False
            
            # Test again after installation
            if not test_dependencies():
                print_error("Dependencies still not working after installation")
                return False
        
        # Test build
        if not test_build():
            print_warning("Build test failed, but you can still try running the dev server")
        
        print_header("SETUP COMPLETE")
        print_success("Frontend setup test completed successfully!")
        print_info("You can now run the development server with:")
        print_info("  cd frontend")
        print_info("  npm run dev")
        print_info("Then visit: http://localhost:3000")
        
        # Ask if user wants to start dev server
        try:
            response = input(f"\n{Colors.YELLOW}Start development server now? (y/n): {Colors.END}")
            if response.lower() in ['y', 'yes']:
                start_dev_server()
        except KeyboardInterrupt:
            print_info("Skipping dev server start")
        
        return True
        
    except Exception as e:
        print_error(f"Frontend test failed: {e}")
        return False
    finally:
        # Return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user{Colors.END}")
        sys.exit(1)