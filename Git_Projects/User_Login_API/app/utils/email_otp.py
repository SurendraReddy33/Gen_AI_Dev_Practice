import smtplib
import random
from email.message import EmailMessage
from app.utils.logger import get_logger
from fastapi import HTTPException
from datetime import datetime,timedelta


logger = get_logger(__name__)
 
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(receiver_email: str, sender_email: str, app_password: str) -> str:
    otp = generate_otp()
    subject = "Your OTP Verification Code"
    body = f"""
    Hello,
 
    Your OTP code is: {otp}

    It will expires in 5 minutes.

    Expire time : {datetime.utcnow()+timedelta(minutes=5)}
 
    Please use this to verify your identity.
 
    - Team
    - User_Auth
    """
 
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)
 
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        logger.info(f" OTP sent successfully to {receiver_email}")
        return otp
    except Exception as e:
        logger.error(f" Failed to send OTP: {e}")
        raise HTTPException(status_code = 500,
                                detail = f"Something went wrong {e}")
    
def send_token(receiver_email: str, sender_email: str, app_password: str , token:str ,username:str) -> str:
    
    subject = "Your JWT Token"
    body = f"""
    Hello {username},

    Login Success.
 
    Your JWT token is:   {token}
    

    It will expires in 1 Hour.

    Expire time : {datetime.utcnow()+timedelta(hours=1)}
 
    Please use this for Authorization.
 
    - Team
    - User_Auth
    """
 
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)
 
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        logger.info(f" OTP sent successfully to {receiver_email}")
        return token
    except Exception as e:
        logger.error(f" Failed to send OTP: {e}")
        raise HTTPException(status_code = 500,
                                detail = f"Something went wrong {e}")