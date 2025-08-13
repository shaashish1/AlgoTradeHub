#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "AlgoTradeHub Frontend Setup"
echo "========================================"
echo

# Check Node.js
echo "Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js found: $NODE_VERSION${NC}"
else
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check npm
echo
echo "Checking npm installation..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✅ npm found: $NPM_VERSION${NC}"
else
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

# Clean previous installation
echo
echo "Cleaning previous installation..."
if [ -d "node_modules" ]; then
    echo "Removing old node_modules..."
    rm -rf node_modules
fi

if [ -f "package-lock.json" ]; then
    echo "Removing old package-lock.json..."
    rm package-lock.json
fi

# Install dependencies
echo
echo "Installing dependencies..."
echo "This may take a few minutes..."

if npm install; then
    echo -e "${GREEN}✅ Dependencies installed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️ npm install failed. Trying with legacy peer deps...${NC}"
    if npm install --legacy-peer-deps; then
        echo -e "${GREEN}✅ Dependencies installed with legacy peer deps!${NC}"
    else
        echo -e "${RED}❌ Installation failed even with legacy peer deps${NC}"
        echo "Please check the error messages above"
        exit 1
    fi
fi

# Test build
echo
echo "Testing build..."
if npm run build; then
    echo -e "${GREEN}✅ Build test successful!${NC}"
else
    echo -e "${YELLOW}⚠️ Build test failed, but you can still try running the dev server${NC}"
fi

echo
echo "========================================"
echo "Frontend Setup Complete!"
echo "========================================"
echo
echo "You can now start the development server with:"
echo "  npm run dev"
echo
echo "The application will be available at:"
echo "  http://localhost:3000"
echo

read -p "Start development server now? (y/n): " choice
if [[ $choice == [Yy]* ]]; then
    echo
    echo "Starting development server..."
    echo "Press Ctrl+C to stop the server"
    echo
    npm run dev
fi

echo
echo "Setup completed successfully!"