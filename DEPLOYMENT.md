# Deployment Guide: Trinity Hostel Management System

## Local Development Setup

### Quick Start
```bash
# 1. Navigate to project
cd hostelredo

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install Django
pip install django

# 4. Run migrations (already done)
python manage.py migrate

# 5. Load fixtures
python manage.py loaddata hostels/fixtures/hostels_and_floors.json hostels/fixtures/rooms.json

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

Access at http://127.0.0.1:8000

## Production Deployment on Render

### Step 1: Prepare Your Project

1. **Update settings.py for production**

Add at the top:
```python
import os
import dj_database_url
from pathlib import Path
```

Replace the entire DATABASES and add these settings:
```python
# SECURITY SETTINGS
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-fallback-key-change-in-production')

# DATABASE
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add whitenoise middleware at the top of MIDDLEWARE
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line first
    'django.middleware.security.SecurityMiddleware',
    # ... rest of middleware
]

# SECURITY
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
```

2. **Create requirements.txt with production packages**

```bash
pip freeze > requirements.txt
```

Then add these packages:
```
gunicorn==21.2.0
dj-database-url==2.1.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
python-decouple==3.8
```

3. **Create build script (render.yaml)**

Create file `render.yaml` in root:
```yaml
services:
  - type: web
    name: trinity-hostel-system
    runtime: python
    pythonVersion: 3.11
    startCommand: gunicorn hostel_management.wsgi:application --bind 0.0.0.0:$PORT
    buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata hostels/fixtures/hostels_and_floors.json hostels/fixtures/rooms.json && python manage.py collectstatic --noinput
    envVars:
      - key: DATABASE_URL
        scope: shared
      - key: DJANGO_SETTINGS_MODULE
        value: hostel_management.settings
      - key: PYTHON_VERSION
        value: 3.11.4
```

4. **Create .gitignore**

```
*.pyc
__pycache__/
*.sqlite3
venv/
.env
staticfiles/
*.egg-info/
dist/
build/
.DS_Store
*.log
```

5. **Initialize git repository and commit**

```bash
git init
git add .
git commit -m "Initial commit: Trinity Hostel Management System"
```

### Step 2: Deploy to Render

1. **Go to https://render.com**
   - Sign up or log in
   - Click "New" > "Web Service"

2. **Connect GitHub Repository**
   - Select "Deploy from GitHub"
   - Authorize and select your repository
   - Select the main branch

3. **Configure Web Service**

   **Name**: `trinity-hostel-system`
   
   **Region**: Choose nearest to your location
   
   **Runtime**: `Python 3`
   
   **Build Command**:
   ```
   pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata hostels/fixtures/hostels_and_floors.json hostels/fixtures/rooms.json && python manage.py collectstatic --noinput
   ```
   
   **Start Command**:
   ```
   gunicorn hostel_management.wsgi:application
   ```

4. **Set Environment Variables**

   Click "Advanced" > "Add Environment Variable"
   
   Add these variables:
   
   | Key | Value |
   |-----|-------|
   | `DJANGO_SUPERUSER_USERNAME` | `admin` |
   | `DJANGO_SUPERUSER_PASSWORD` | `your_secure_password_here` |
   | `DJANGO_SUPERUSER_EMAIL` | `admin@trinity.edu` |
   | `SECRET_KEY` | Generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
   | `DATABASE_URL` | Leave empty (Render provides) |

   **Create PostgreSQL database** (if not using Render PostgreSQL):
   - Render > New > PostgreSQL
   - Connect to your web service
   - Copy DATABASE_URL environment variable

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete (5-10 minutes)
   - Check deployment logs if there are issues

### Step 3: Post-Deployment Setup

1. **Access Your App**
   - Visit: `https://your-app-name.onrender.com`
   - Admin panel: `https://your-app-name.onrender.com/admin`

2. **Create Initial Admin User** (if not done via env vars)
   ```bash
   render exec python manage.py createsuperuser
   ```

3. **Verify Fixtures Loaded**
   - Login to admin panel
   - Check if hostels, floors, and rooms are visible

### Step 4: Maintenance

**View Logs**
```bash
render logs --service trinity-hostel-system
```

**SSH into Service**
```bash
render shell --service trinity-hostel-system
```

**Backup Database**
- Use Render's database backup feature
- Regular manual exports recommended

**Update Code**
```bash
git push origin main
# Render automatically redeploys on push
```

## Production Checklist

- [ ] DEBUG = False in production settings
- [ ] ALLOWED_HOSTS configured correctly
- [ ] SECRET_KEY changed from default
- [ ] Database backed up
- [ ] Email settings configured (optional)
- [ ] HTTPS enabled (Render provides by default)
- [ ] Static files collected (`collectstatic`)
- [ ] Admin user created
- [ ] Test all main workflows
- [ ] Monitor error logs

## Troubleshooting Production Issues

### Issue: Database migrations fail on deploy
**Solution**: Check if database URL is set, run migrations manually via Render shell

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic --noinput`

### Issue: Fixtures not loading
**Solution**: Verify fixture paths in build command, check for import errors

### Issue: 500 errors in production
**Solution**: Check Render logs, verify environment variables, check database connection

### Issue: Email not sending
**Solution**: Configure email backend in settings.py (optional for this app)

## Scaling for Large Users

### Database
- Render PostgreSQL scales automatically
- Monitor database metrics in Render dashboard
- Consider read replicas for heavy load

### Application
- Upgrade from free tier to higher tier (better CPU/RAM)
- Use Render's auto-scaling feature
- Monitor application metrics

### Static Files
- Use Render's edge locations
- Consider CDN for high traffic

## Security Best Practices

1. **Regular Updates**
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

2. **Database Backups**
   - Enable automated backups in Render
   - Test restore procedures regularly

3. **Environment Variables**
   - Never commit secrets to git
   - Use Render's environment variables
   - Rotate SECRET_KEY periodically

4. **Access Control**
   - Strong admin passwords
   - Regular user audit
   - Disable inactive accounts

5. **HTTPS**
   - Always enforced (Render default)
   - Update SECURE_SSL_REDIRECT

## Support & Documentation

- Django Documentation: https://docs.djangoproject.com/en/5.2/
- Render Documentation: https://render.com/docs
- PostgreSQL: https://www.postgresql.org/docs/
