#!/bin/bash

# Render Deployment Preparation Script
# This script helps prepare your Trinity Hostel Management System for Render deployment

echo "================================"
echo "Render Deployment Preparation"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Creating template..."
    cp .env.example .env 2>/dev/null || echo "# Create .env file manually with Render configuration" > .env
fi

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate

# Check Django configuration
echo "✅ Verifying Django configuration..."
python manage.py check --deploy

echo ""
echo "================================"
echo "Pre-Deployment Checklist"
echo "================================"
echo ""
echo "Before pushing to Render:"
echo ""
echo "1. ✅ Update ALLOWED_HOSTS in .env:"
echo "   ALLOWED_HOSTS=localhost,127.0.0.1,your-app-name.onrender.com"
echo ""
echo "2. ✅ Update CORS_ALLOWED_ORIGINS in .env:"
echo "   CORS_ALLOWED_ORIGINS=https://your-app-name.onrender.com"
echo ""
echo "3. ✅ Generate a new SECRET_KEY:"
python -c "from django.core.management.utils import get_random_secret_key; print(f'   SECRET_KEY={get_random_secret_key()}')"
echo ""
echo "4. ✅ Create PostgreSQL database on Render"
echo ""
echo "5. ✅ Push to GitHub with updated settings"
echo ""
echo "6. ✅ Connect GitHub repo to Render and deploy"
echo ""
echo "7. ✅ Set environment variables in Render dashboard"
echo ""
echo "8. ✅ Create superuser after deployment:"
echo "   python manage.py createsuperuser"
echo ""
echo "================================"
echo "Deployment Commands"
echo "================================"
echo ""
echo "Build Command (Render):"
echo "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
echo ""
echo "Start Command (Render):"
echo "gunicorn hostel_management.wsgi:application --bind 0.0.0.0:\$PORT"
echo ""
echo "================================"
echo "For detailed instructions, see: RENDER_DEPLOYMENT.md"
echo "================================"
