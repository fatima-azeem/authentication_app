import asyncio
import logging
from app.core.config import settings
import resend

resend.api_key = settings.RESEND_API_KEY


async def send_verification_email(email: str, otp: str) -> None:
    """
    Sends a verification email with the provided OTP to the specified email address using Resend.
    Args:
        email (str): Recipient's email address.
        otp (str): One-time password to include in the email.
    Raises:
        Exception: If sending the email fails.
    """
    subject = "Your Verification Code"
    html_content = f"""
    <p>Hello,</p>
    <p>Your verification code is: <strong>{otp}</strong></p>
    <p>If you did not request this, please ignore this email.</p>
    """
    params = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [email],
        "subject": subject,
        "html": html_content,
    }
    try:
        result = await asyncio.to_thread(resend.Emails.send, params)  # type:ignore
        logging.info(f"Verification email sent to {email}: {result}")
        logging.debug(f"OTP sent to {email}: {otp}")
    except Exception as e:
        logging.error(f"Failed to send verification email to {email}: {e}")
        raise


async def send_password_reset_email(email: str, otp: str) -> None:
    """
    Sends a password reset OTP to the specified email address using Resend.
    Args:
        email (str): Recipient's email address.
        otp (str): One-time password to include in the email.
    Raises:
        Exception: If sending the email fails.
    """
    subject = "Password Reset OTP"
    html_content = f"""
    <p>Hello,</p>
    <p>You requested a password reset. Your OTP is: <strong>{otp}</strong></p>
    <p>If you did not request this, please ignore this email.</p>
    """
    params = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [email],
        "subject": subject,
        "html": html_content,
    }
    try:
        result = await asyncio.to_thread(resend.Emails.send, params)  # type:ignore
        logging.info(f"Password reset OTP sent to {email}: {result}")
        logging.debug(f"Password reset OTP sent to {email}: {otp}")
    except Exception as e:
        logging.error(f"Failed to send password reset OTP to {email}: {e}")
        raise


# send_verification_email already exists and is used for OTP delivery.
# No changes needed for OTP-based password reset.
