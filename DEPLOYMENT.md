# Deployment Guide

## Project Structure (Updated)

```
CUET-Medical-Center/
├── backend/                 # Django backend apps
│   ├── accounts/           # User authentication
│   ├── bloodbank/          # Blood bank management
│   ├── notifications/      # Notices and alerts
│   ├── records/            # Medical records
│   ├── roster/             # Doctor roster
│   └── cuet_medical/       # Django project settings
├── frontend/               # Frontend application
│   ├── assets/             # CSS, JS, images
│   ├── student/            # Student-specific pages
│   └── *.html              # HTML pages
├── media/                  # User uploads (notices, PDFs)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── DEPLOYMENT.md          # This file
```

## Running Locally

### Prerequisites
- Python 3.8+
- pip
- Virtual Environment

### Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/mahfuz-byte/CUET-Medical-Center.git
   cd CUET-Medical-Center
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Mac/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access Application**
   - Main App: `http://127.0.0.1:8000`
   - Login Page: `http://127.0.0.1:8000/login.html`
   - Admin Panel: `http://127.0.0.1:8000/admin`

## GitHub Deployment Options

### Option 1: Heroku Deployment (Recommended for Full Stack)

1. **Create Heroku Account**
   - Go to https://www.heroku.com

2. **Install Heroku CLI**
   ```bash
   # Windows
   Download from https://devcenter.heroku.com/articles/heroku-cli
   
   # Mac/Linux
   brew install heroku/brew/heroku
   ```

3. **Create Procfile**
   ```
   web: gunicorn cuet_medical.wsgi
   ```

4. **Create runtime.txt**
   ```
   python-3.9.16
   ```

5. **Push to Heroku**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   ```

### Option 2: GitHub Pages + External API (Frontend Only)

1. **Create `docs/` folder with static files**
   ```bash
   mkdir docs
   cp -r frontend/* docs/
   ```

2. **Update API URLs in JavaScript**
   - Change all API calls to point to deployed backend
   - Example: `https://your-api.herokuapp.com/api/...`

3. **Configure GitHub Pages**
   - Go to Repository Settings → Pages
   - Source: Deploy from branch
   - Branch: `main`, folder: `/docs`

### Option 3: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   CMD ["gunicorn", "cuet_medical.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

2. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "8000:8000"
       environment:
         - DEBUG=False
   ```

3. **Build and Run**
   ```bash
   docker-compose up
   ```

## Environment Variables

Create `.env` file (already in `.gitignore`):

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
GROQ_API_KEY=your-groq-api-key
```

## Database Considerations

### Development
- SQLite (current) - Good for single-user testing

### Production
- PostgreSQL recommended
- Update `DATABASES` in `settings.py`:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'your_db_name',
          'USER': 'your_db_user',
          'PASSWORD': 'your_db_password',
          'HOST': 'your_db_host',
          'PORT': '5432',
      }
  }
  ```

## Important Files for Deployment

- **settings.py** - Update `DEBUG=False` and `ALLOWED_HOSTS` for production
- **requirements.txt** - All Python dependencies
- **manage.py** - Django management commands
- **cuet_medical/wsgi.py** - WSGI application for production servers

## Static Files & Media

### Collect Static Files
```bash
python manage.py collectstatic
```

### Media Files
- Current: Stored in `/media` folder
- Production: Use cloud storage (AWS S3, Google Cloud Storage, etc.)

## SSL/HTTPS

- Enable in production server configuration
- Update `SECURE_SSL_REDIRECT=True` in settings for production

## Monitoring & Logging

- Use Django logging framework
- Consider: Sentry, LogRocket for error tracking
- Monitor: Server health, database performance, API response times

## Backup Strategy

- Regular database backups
- Version control commits to GitHub
- Cloud backup for uploaded files (notices, PDFs)

## Support

For deployment issues or questions:
- Check Django deployment checklist: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
- Review Heroku Python guide: https://devcenter.heroku.com/articles/python-support

---

**Last Updated:** April 26, 2026
