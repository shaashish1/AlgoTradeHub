@echo off
echo ========================================
echo AlgoTradeHub Frontend Setup
echo ========================================
echo.

echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js found: 
node --version

echo.
echo Checking npm installation...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ npm found: 
npm --version

echo.
echo Cleaning previous installation...
if exist node_modules (
    echo Removing old node_modules...
    rmdir /s /q node_modules
)

if exist package-lock.json (
    echo Removing old package-lock.json...
    del package-lock.json
)

echo.
echo Installing dependencies...
echo This may take a few minutes...
npm install

if %errorlevel% neq 0 (
    echo.
    echo ❌ npm install failed. Trying with legacy peer deps...
    npm install --legacy-peer-deps
    
    if %errorlevel% neq 0 (
        echo ❌ Installation failed even with legacy peer deps
        echo Please check the error messages above
        pause
        exit /b 1
    )
)

echo.
echo ✅ Dependencies installed successfully!

echo.
echo Testing build...
npm run build

if %errorlevel% neq 0 (
    echo ⚠️ Build test failed, but you can still try running the dev server
) else (
    echo ✅ Build test successful!
)

echo.
echo ========================================
echo Frontend Setup Complete!
echo ========================================
echo.
echo You can now start the development server with:
echo   npm run dev
echo.
echo The application will be available at:
echo   http://localhost:3000
echo.

set /p choice="Start development server now? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo Starting development server...
    echo Press Ctrl+C to stop the server
    echo.
    npm run dev
)

echo.
echo Setup completed successfully!
pause