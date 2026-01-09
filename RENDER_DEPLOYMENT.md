# Render Deployment Guide - Trinity Hostel Management System

## Prerequisites

1. **Render Account**: Sign up at https://render.com
2. **GitHub Repository**: Push your code to GitHub
3. **PostgreSQL Database**: Create a PostgreSQL instance on Render
4. **Environment Variables**: Prepare all secrets

---

## Step 1: Create PostgreSQL Database on Render

1. Go to **Render Dashboard** → **New +** → **PostgreSQL**
2. Fill in:
   - **Name**: `trinity-hostel-db`
   - **Database**: `hostel_management`
   - **User**: Your preferred username
   - **Region**: Select your region
   - **Plan**: Free (or paid if needed)
3. Click **Create Database**
4. Wait for creation and note the **Database URL**

---

## Step 2: Deploy Web Service

### Option A: Using GitHub Integration

1. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. In **Render Dashboard** → **New +** → **Web Service**

3. Connect your GitHub repository:
   - Select your repository
   - Click **Connect**

4. Configure the service:
   - **Name**: `trinity-hostel-management`
   - **Environment**: `Python 3`
   - **Build Command**:
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**:
     ```
     gunicorn hostel_management.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Free (or paid)

5. Click **Create Web Service**

### Option B: Using render.yaml

If using `render.yaml`:
1. Push to GitHub with `render.yaml` in root
2. In Render Dashboard → **New +** → **Web Service**
3. Select your GitHub repo → Connect
4. Render will auto-detect `render.yaml` configuration

---

## Step 3: Set Environment Variables

In the **Web Service Settings**:

1. Go to **Environment** tab
2. Add these variables:

```
DEBUG=False
SECRET_KEY=<your-secret-key-from-.env>
ALLOWED_HOSTS=your-service-name.onrender.com
DATABASE_URL=<postgresql-url-from-step-1>
CORS_ALLOWED_ORIGINS=https://your-service-name.onrender.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

3. Click **Save**

---

## Step 4: Database Configuration

The app uses `DATABASE_URL` for PostgreSQL. Update your `.env`:

```
# For Render PostgreSQL
DATABASE_URL=postgresql://username:password@your-database-host.onrender.com:5432/hostel_management
```

The `settings.py` will automatically detect and use PostgreSQL.

---

## Step 5: Create Superuser

After first deployment:

1. In **Web Service** → **Shell**:
   ```bash
   python manage.py createsuperuser
   ```

2. Enter admin credentials when prompted

---

## Step 6: Load Initial Data (Optional)

To load sample data:

```bash
# In Render Shell
python manage.py loaddata fixtures/initial_data.json
```

---

## Step 7: Run Final Tests

1. Visit your app: `https://your-service-name.onrender.com`
2. Access admin panel: `https://your-service-name.onrender.com/admin`
3. Test login with matric number
4. Submit and approve a hostel request

---

## Common Issues & Solutions

### Issue: Static Files Not Loading

**Solution**: 
```bash
# Run in Render Shell
python manage.py collectstatic --noinput
```

Restart the service afterward.

### Issue: Database Connection Error

**Solution**: 
- Verify `DATABASE_URL` is correct in environment variables
- Check PostgreSQL instance is running
- Ensure IP is whitelisted

### Issue: Redirect Loop on Login

**Solution**:
- Update `ALLOWED_HOSTS` with your Render domain
- Clear browser cookies for the domain
- Restart the service

### Issue: CORS Errors

**Solution**:
- Add your frontend URL to `CORS_ALLOWED_ORIGINS`
- Ensure `DEBUG=False` and `SECURE_SSL_REDIRECT=True` match

### Issue: 500 Internal Server Error

**Solution**:
1. Check logs in Render: **Web Service** → **Logs**
2. Look for specific error messages
3. Update `.env` variables if needed
4. Redeploy

---

## White Noise Configuration

WhiteNoise is configured automatically for static file serving:

- **Compression**: Enabled via `CompressedManifestStaticFilesStorage`
- **Caching**: Static files are cached by browser
- **CDN**: Render's CDN automatically serves static files

---

## Security Checklist

✅ `DEBUG=False` in production  
✅ `SECURE_SSL_REDIRECT=True`  
✅ `SESSION_COOKIE_SECURE=True`  
✅ `CSRF_COOKIE_SECURE=True`  
✅ Strong `SECRET_KEY` generated  
✅ `ALLOWED_HOSTS` properly configured  
✅ `CORS_ALLOWED_ORIGINS` restricted  
✅ Database credentials kept in environment variables  
✅ `.env` not committed to Git  
✅ PostgreSQL SSL connection enabled  

---

## Monitoring & Logs

### View Logs

In **Web Service Settings**:
- **Logs** tab shows real-time application logs
- **Events** tab shows deployment history

### Common Log Messages

```
# Normal startup
Starting gunicorn...
Application loaded successfully
```

```
# Static files collection
Collecting static files...
```

---

## Scaling & Performance

For production use:

1. **Upgrade Plan**: Free → Starter/Standard
2. **PostgreSQL**: Upgrade from free tier
3. **CDN**: Enable Render's CDN for static files
4. **Auto-scaling**: Available on paid plans

---

## Environment Variable Reference

| Variable | Value | Notes |
|----------|-------|-------|
| `DEBUG` | `False` | Always False in production |
| `SECRET_KEY` | Generate new one | Keep secure |
| `ALLOWED_HOSTS` | Your domain | e.g., app.onrender.com |
| `DATABASE_URL` | PostgreSQL URL | From Render PostgreSQL |
| `CORS_ALLOWED_ORIGINS` | Your domain | https://app.onrender.com |
| `SECURE_SSL_REDIRECT` | `True` | Forces HTTPS |
| `SESSION_COOKIE_SECURE` | `True` | Secure cookies only |
| `CSRF_COOKIE_SECURE` | `True` | Secure CSRF only |

---

## Quick Reference Commands

```bash
# Connect to database
psql $DATABASE_URL

# Dump database backup
pg_dump $DATABASE_URL > backup.sql

# Restore database
psql $DATABASE_URL < backup.sql

# Check migrations status
python manage.py showmigrations

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Django Docs**: https://docs.djangoproject.com
- **WhiteNoise Docs**: https://whitenoise.readthedocs.io
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

**Your app is now production-ready on Render! 🚀**
