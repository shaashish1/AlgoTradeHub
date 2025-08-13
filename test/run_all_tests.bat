@echo off
echo ========================================
echo AlgoTradeHub - Complete System Test
echo ========================================
echo.

echo Testing Python Backend...
echo ----------------------------------------
python test_all_systems.py

echo.
echo.
echo Testing Frontend Setup...
echo ----------------------------------------
python test_frontend_setup.py

echo.
echo.
echo ========================================
echo All tests completed!
echo ========================================
echo.
echo Next steps:
echo 1. If backend tests passed: python main.py
echo 2. If frontend tests passed: cd frontend && npm run dev
echo 3. Web interface: python app.py
echo.
pause