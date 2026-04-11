# Email Configuration Guide for OTP Feature

## Overview
The signup feature requires email configuration to send OTPs. Follow these steps to set up email sending.

## Option 1: Gmail Setup (Recommended)

### Step 1: Enable 2-Factor Authentication on Gmail
1. Go to https://myaccount.google.com/
2. Click "Security" on the left sidebar
3. Find "2-Step Verification" and enable it
4. Verify your phone number and complete setup

### Step 2: Create App Password
1. Go back to Security settings
2. Find "App passwords" (appears after enabling 2FA)
3. Select "Mail" and "Windows Computer" (or your device)
4. Google will generate a 16-character password - **copy it**

### Step 3: Add to .env file
Create or edit `.env` file in the project root (D:/My Downloads/IP Project/CUET-Medical-Center/):

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
```

Replace:
- `your-gmail@gmail.com` with your Gmail address
- `xxxx xxxx xxxx xxxx` with the 16-character app password (with spaces)

### Step 4: Test Email Configuration
Run this in your Django shell to verify:
```bash
python manage.py shell
```

Then in the Python shell:
```python
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email.',
    'your-gmail@gmail.com',
    ['recipient@example.com'],
    fail_silently=False,
)
```

If successful, an email will be sent.

---

## Option 2: Other Email Services

### SendGrid
```
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=your_sendgrid_api_key
```

### Mailgun
```
EMAIL_BACKEND=anymail.backends.mailgun.EmailBackend
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_SENDER_DOMAIN=your_mailgun_domain
```

---

## Important Notes

1. **Don't use plain Gmail password** - Always use App Password for security
2. **Keep .env file private** - Add it to `.gitignore`
3. **Test before deployment** - Send test OTP before going live
4. **Rate limits** - Free Gmail has limits (~500 emails/day)

---

## API Endpoints

Once email is configured, the following endpoints are available:

### 1. Send OTP
**POST** `/api/auth/send-otp/`
```json
{
    "email": "student@cuet.ac.bd",
    "role": "student"  // or "doctor"
}
```

### 2. Verify OTP
**POST** `/api/auth/verify-otp/`
```json
{
    "email": "student@cuet.ac.bd",
    "otp_code": "12345"
}
```

### 3. Signup (Complete Registration)
**POST** `/api/auth/signup/`
```json
{
    "email": "student@cuet.ac.bd",
    "first_name": "John Doe",
    "password": "mypassword123",
    "otp_code": "12345"
}
```

### 4. Login
**POST** `/api/auth/login/`
```json
{
    "email": "student@cuet.ac.bd",
    "password": "mypassword123"
}
```

---

## Database Notes

The OTP and User data is stored in SQLite:
- **OTP Model**: Stores email, OTP code, role, creation time, expiry time, usage status
- **User Model**: Stores email, plaintext password, name, role, is_active status
- OTPs expire after 5 minutes
- Each OTP can only be used once

---

## Troubleshooting

If OTP emails are not sending:

1. **Check Django Logs**: Look for error messages in terminal
2. **Verify Email Credentials**: Double-check .env file values
3. **Check Gmail Security**: Login to Gmail and check for suspicious activity alerts
4. **Test SMTP Connection**:
```bash
python -m smtplib -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587).starttls()"
```

5. **Enable Less Secure Apps** (if using Gmail password instead of App Password):
   - Go to https://myaccount.google.com/lesssecureapps
   - Enable "Less secure app access"
   - (Not recommended - use App Password instead)
