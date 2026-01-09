@echo off
REM Render Deployment Preparation Script for Windows
REM This script helps prepare Trinity Hostel Management System for Render deployment

echo ================================
echo Render Deployment Preparation
echo ================================
echo.

REM Check if .env exists
if not exist .env (
    echo # .env file for Render deployment > .env
    echo DEBUG=False >> .env
    echo SECRET_KEY=your-secret-key-here >> .env
    echo ALLOWED_HOSTS=localhost,127.0.0.1,your-app-name.onrender.com >> .env
    echo CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com >> .env
)

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo.
echo 1. Installing dependencies...
pip install -r requirements.txt

echo.
echo 2. Collecting static files...
python manage.py collectstatic --noinput --clear

echo.
echo 3. Running migrations...
python manage.py migrate

echo.
echo 4. Verifying Django configuration...
python manage.py check --deploy

echo.
echo ================================
echo Pre-Deployment Checklist
echo ================================
echo.
echo Before pushing to Render:
echo.
echo 1. Update ALLOWED_HOSTS in .env:
echo    ALLOWED_HOSTS=localhost,127.0.0.1,your-app-name.onrender.com
echo.
echo 2. Update CORS_ALLOWED_ORIGINS in .env:
echo    CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com
echo.
echo 3. Generate a new SECRET_KEY and update .env
python -c "from django.core.management.utils import get_random_secret_key; print(f'   SECRET_KEY={get_random_secret_key()}')"
echo.
echo 4. Create PostgreSQL database on Render
echo.
echo 5. Push to GitHub with updated settings
echo.
echo 6. Connect GitHub repo to Render and deploy
echo.
echo 7. Set environment variables in Render dashboard
echo.
echo 8. Create superuser after deployment:
echo    python manage.py createsuperuser
echo.
echo ================================
echo Deployment Commands for Render
echo ================================
echo.
echo Build Command:
echo pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
echo.
echo Start Command:
echo gunicorn hostel_management.wsgi:application --bind 0.0.0.0:%PORT%
echo.
echo ================================
echo For detailed instructions, see: RENDER_DEPLOYMENT.md
echo ================================
echo.
pause
