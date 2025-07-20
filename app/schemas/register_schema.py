from pydantic import BaseModel, EmailStr, Field, validator
import re
from typing import Optional


class RegisterSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(
        ..., 
        min_length=8,
        description="Password must meet complexity requirements"
    )
    is_term_accepted: bool
    
    @validator('password')
    def validate_password_strength(cls, password: str) -> str:
        """
        Validate password meets security requirements:
        - At least 8 characters long
        - At least one uppercase letter (A–Z)
        - At least one lowercase letter (a–z)
        - At least one digit (0–9)
        - At least one special character (!@#$%^&*()_+{}[]:;<>,.?~)
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must include at least one uppercase letter (A-Z)")
        
        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must include at least one lowercase letter (a-z)")
        
        # Check for digit
        if not re.search(r'\d', password):
            raise ValueError("Password must include at least one digit (0-9)")
        
        # Check for special character
        special_chars = r'[!@#$%^&*()_+{}[\]:;<>,.?~]'
        if not re.search(special_chars, password):
            raise ValueError("Password must include at least one special character (!@#$%^&*()_+{}[]:;<>,.?~)")
        
        # Check for common weak patterns
        weak_patterns = [
            r'123456', r'password', r'qwerty', r'abc123',
            r'admin', r'letmein', r'welcome', r'monkey'
        ]
        
        password_lower = password.lower()
        for pattern in weak_patterns:
            if re.search(pattern, password_lower):
                raise ValueError("Password contains common weak pattern. Please choose a more secure password")
        
        # Check for sequential characters
        if cls._has_sequential_chars(password):
            raise ValueError("Password should not contain sequential characters (e.g., abc, 123)")
        
        # Check for repetitive characters
        if cls._has_repetitive_chars(password):
            raise ValueError("Password should not contain repetitive characters (e.g., aaa, 111)")
        
        return password
    
    @staticmethod
    def _has_sequential_chars(password: str, min_sequence: int = 3) -> bool:
        """Check for sequential characters like 'abc' or '123'"""
        password_lower = password.lower()
        
        # Check for alphabetical sequences
        for i in range(len(password_lower) - min_sequence + 1):
            sequence = password_lower[i:i + min_sequence]
            if len(sequence) >= min_sequence:
                is_sequence = True
                for j in range(len(sequence) - 1):
                    if ord(sequence[j + 1]) != ord(sequence[j]) + 1:
                        is_sequence = False
                        break
                if is_sequence:
                    return True
        
        # Check for numerical sequences
        for i in range(len(password) - min_sequence + 1):
            sequence = password[i:i + min_sequence]
            if sequence.isdigit():
                nums = [int(c) for c in sequence]
                is_sequence = True
                for j in range(len(nums) - 1):
                    if nums[j + 1] != nums[j] + 1:
                        is_sequence = False
                        break
                if is_sequence:
                    return True
        
        return False
    
    @staticmethod
    def _has_repetitive_chars(password: str, max_repeat: int = 3) -> bool:
        """Check for repetitive characters like 'aaa' or '111'"""
        for i in range(len(password) - max_repeat + 1):
            if len(set(password[i:i + max_repeat])) == 1:
                return True
        return False
    
    @validator('full_name')
    def validate_full_name(cls, name: str) -> str:
        """Validate full name doesn't contain invalid characters"""
        if not re.match(r'^[a-zA-Z\s\-\.\']+$', name.strip()):
            raise ValueError("Full name can only contain letters, spaces, hyphens, dots, and apostrophes")
        
        # Check for reasonable length after stripping
        stripped_name = name.strip()
        if len(stripped_name) < 2:
            raise ValueError("Full name must be at least 2 characters long")
        
        return stripped_name
    
    @validator('email')
    def validate_email_format(cls, email: str) -> str:
        """Additional email validation"""
        email = email.lower().strip()
        
        # Check for common disposable email domains (optional security measure)
        disposable_domains = [
            "10minutemail.com", "tempmail.org", "guerrillamail.com",
            "mailinator.com", "throwaway.email"
        ]
        
        domain = email.split('@')[1] if '@' in email else ""
        if domain in disposable_domains:
            raise ValueError("Disposable email addresses are not allowed")
        
        return email


class RegisterResponse(BaseModel):
    message: str
    user_id: Optional[str] = None
    email: str


class ResendOtpSchema(BaseModel):
    email: EmailStr


class ResendOtpResponse(BaseModel):
    message: str