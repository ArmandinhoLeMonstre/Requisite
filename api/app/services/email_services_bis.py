import os
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FRONTEND_URL = os.getenv("FRONTEND_URL")

async def send_email_bis(to_send: str, confirmation_token: str):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_send
    msg["Subject"] = "Requisit verification link"
    body = f"""
                <div style="max-width:560px; margin:0 auto; font-family:Arial, sans-serif; background:#ffffff; border-radius:12px; overflow:hidden; border:1px solid #e5e7eb;">
                    <div style="height:4px; background:#4F46E5;"></div>
                    <div style="padding:3rem 2.5rem 2rem;">
                        <h2 style="font-size:20px; font-weight:500; color:#1a1a1a; margin:0 0 1.5rem;">Verify your email address</h2>
                        <p style="font-size:14px; color:#6b7280; margin:0 0 2.5rem; line-height:1.8;">
                            Welcome to Requisite. Click the button below to verify your email address and activate your account.
                        </p>
                        <a href="{FRONTEND_URL}/verify/{confirmation_token}"
                        style="display:inline-block; background:#4F46E5; color:white; padding:14px 32px; border-radius:8px; text-decoration:none; font-size:14px; font-weight:500;">
                            Verify my email
                        </a>
                        <div style="margin-top:3rem; padding-top:2rem; border-top:1px solid #e5e7eb;">
                            <p style="font-size:12px; color:#9ca3af; margin:0 0 1rem; line-height:1.8;">
                                If the button doesn't work, copy and paste this link into your browser:<br>
                                <span style="color:#4F46E5; word-break:break-all;">{FRONTEND_URL}/verify/{confirmation_token}</span>
                            </p>
                            <p style="font-size:12px; color:#9ca3af; margin:0;">
                                <em>If you did not create an account, you can safely ignore this email.</em>
                            </p>
                        </div>
                    </div>
                </div>
                """
    msg.attach(MIMEText(body, "html"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True
        )
        return True
    except Exception:
        raise
    