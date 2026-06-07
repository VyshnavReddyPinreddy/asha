from email.message import EmailMessage
import aiosmtplib

from core.config import settings

async def send_otp_email(email:str,otp:str):

    msg = EmailMessage()
    msg["Subject"] = "Password Reset OTP"
    msg["From"] = settings.SENDER_EMAIL
    msg["To"] = email 

    msg.set_content(
        f"""
Your password reset OTP is : {otp}

Valid for 10 minutes. 
        """
    ) 

    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )
