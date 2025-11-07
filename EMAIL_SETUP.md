# Email OTP Setup Guide

This guide will help you configure email settings for the OTP verification feature in SmartHire.

## Prerequisites

1. Install Flask-Mail:
```bash
pip install Flask-Mail==0.9.1
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Email Configuration

### Option 1: Using Gmail (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to your Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Copy the 16-character password

3. **Set Environment Variables** (Recommended):
   ```bash
   # Windows (PowerShell)
   $env:MAIL_USERNAME="your-email@gmail.com"
   $env:MAIL_PASSWORD="your-16-char-app-password"
   
   # Windows (CMD)
   set MAIL_USERNAME=your-email@gmail.com
   set MAIL_PASSWORD=your-16-char-app-password
   
   # Linux/Mac
   export MAIL_USERNAME="your-email@gmail.com"
   export MAIL_PASSWORD="your-16-char-app-password"
   ```

4. **Or Update app.py directly** (Less secure):
   - Open `app.py`
   - Find the email configuration section (around line 50)
   - Replace `'your-email@gmail.com'` with your email
   - Replace `'your-app-password'` with your app password

### Option 2: Using Other Email Providers

Update the email configuration in `app.py`:

```python
# For Outlook/Hotmail
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587

# For Yahoo
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 587

# For Custom SMTP
app.config['MAIL_SERVER'] = 'smtp.yourdomain.com'
app.config['MAIL_PORT'] = 587  # or 465 for SSL
app.config['MAIL_USE_TLS'] = True  # or False for SSL
```

## Testing Email Configuration

1. Start your Flask application
2. Try signing up with a test email
3. Check if you receive the OTP email
4. If not, check the console for error messages

## Troubleshooting

### "Authentication failed" error
- Make sure you're using an App Password, not your regular Gmail password
- Verify 2-Factor Authentication is enabled

### "Connection refused" error
- Check your internet connection
- Verify the SMTP server and port are correct
- Check if your firewall is blocking the connection

### Email not received
- Check spam/junk folder
- Verify the email address is correct
- Check console logs for errors
- Make sure Flask-Mail is properly installed

## Security Notes

- **Never commit email credentials to version control**
- Use environment variables for sensitive information
- Consider using a dedicated email account for your application
- For production, use a professional email service (SendGrid, Mailgun, etc.)

## Production Recommendations

For production environments, consider using:
- **SendGrid** (Free tier: 100 emails/day)
- **Mailgun** (Free tier: 5,000 emails/month)
- **Amazon SES** (Pay-as-you-go)
- **Postmark** (Free tier: 100 emails/month)

These services provide better deliverability and analytics.


