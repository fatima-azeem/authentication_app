import secrets


def generate_otp() -> str:
    """
    Generate a secure random 6-digit numeric OTP code as a string.
    :return: 6-digit OTP code as a string.
    """
    return str(secrets.randbelow(900000) + 100000)
