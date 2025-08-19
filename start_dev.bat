@echo off
echo Starting Habitica Manager (Development Server)
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting Flask development server...
python run.py

echo.
echo Server stopped.
pause
