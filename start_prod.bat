@echo off
echo Starting Habitica Manager (Production Server with Gunicorn)
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing/updating Gunicorn...
pip install gunicorn

echo.
echo Starting Gunicorn server...
gunicorn -c gunicorn.conf.py habitica_manager.app:app

echo.
echo Server stopped.
pause
