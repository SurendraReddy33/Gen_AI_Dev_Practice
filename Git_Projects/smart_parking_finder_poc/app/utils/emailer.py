
import smtplib
from email.message import EmailMessage
from app.config.settings import settings

async def send_mail(to_email: str, subject: str, body: str) -> None:
    # simple SMTP stub; for local dev you can run: python -m smtpd -c DebuggingServer -n localhost:1025
    msg = EmailMessage()
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USER and settings.SMTP_PASS:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg)
    except Exception:
        # In POC, ignore email errors silently
        pass
