#!/usr/bin/env python3
"""
Node.js Installation Checker
Checks if Node.js is installed and provides installation guidance
"""

import subprocess
import sys
import webbrowser
import os

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

def check_nodejs():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            version_num = int(version.replace('v', '').split('.')[0])
            
            print_success(f"Node.js is installed: {version}")
            
            if version_num >= 18:
                print_success("Node.js version is adequate (18+)")
                return True, version
            else:
                print_warning(f"Node.js version {version} is too old (need 18+)")
                return False, version
        else:
            return False, None
    except Exception:
        return False, None

def check_npm():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"npm is installed: {version}")
            return True, version
        else:
            return False, None
    except Exception:
        return False, None

def main():
    """Main function"""
    print_header("NODE.JS INSTALLATION CHECKER")
    
    # Check Node.js
    node_installed, node_version = check_nodejs()
    
    # Check npm
    if node_installed:
        npm_installed, npm_version = check_npm()
    else:
        npm_installed = False
        npm_version = None
    
    print_header("RESULTS")
    
    if node_installed and npm_installed:
        print_success("🎉 Node.js and npm are properly installed!")
        print_info(f"Node.js: {node_version}")
        print_info(f"npm: {npm_version}")
        print_info("")
        print_info("You can now run the frontend fix:")
        print_info("  python fix_frontend.py")
        return True
    else:
        print_error("❌ Node.js is not installed or not working properly")
        print_header("INSTALLATION INSTRUCTIONS")
        
        print_info("To install Node.js:")
        print_info("1. Visit: https://nodejs.org/")
        print_info("2. Download the LTS version (recommended)")
        print_info("3. Run the installer")
        print_info("4. Restart your command prompt")
        print_info("5. Run this script again to verify")
        print_info("")
        
        # Ask if user wants to open the website
        try:
            response = input(f"{Colors.YELLOW}Open Node.js website now? (y/n): {Colors.END}")
            if response.lower() in ['y', 'yes']:
                print_info("Opening https://nodejs.org/ in your browser...")
                webbrowser.open('https://nodejs.org/')
        except KeyboardInterrupt:
            print_info("Skipping website open")
        
        print_header("ALTERNATIVE INSTALLATION METHODS")
        
        print_info("Windows Package Managers:")
        print_info("• Chocolatey: choco install nodejs")
        print_info("• Winget: winget install OpenJS.NodeJS")
        print_info("")
        print_info("After installation:")
        print_info("1. Restart your command prompt")
        print_info("2. Run: node --version")
        print_info("3. Run: npm --version")
        print_info("4. Run: python fix_frontend.py")
        
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Check interrupted by user{Colors.END}")
        sys.exit(1)