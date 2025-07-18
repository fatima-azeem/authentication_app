#!/usr/bin/env python3
"""
Test script to verify password reset functionality.
"""

import asyncio
import asyncpg
from app.db.database import get_db_session
from app.db.models.user_model import User
from app.services.password_reset_service import request_password_reset, reset_password
from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def test_password_reset():
    """Test the password reset flow."""
    
    # Create a database session
    async for db in get_db_session():
        try:
            # Create a test user
            test_email = "test@example.com"
            original_password = "TestPassword123!"
            
            # Check if user exists, if not create one
            result = await db.execute(select(User).where(User.email == test_email))
            user = result.scalar_one_or_none()
            
            if not user:
                user = User(
                    email=test_email,
                    password=argon2.hash(original_password),
                    is_email_verified=True,
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)
                print(f"Created test user: {test_email}")
            else:
                # Update password to known value
                user.password = argon2.hash(original_password)
                await db.commit()
                print(f"Updated test user password: {test_email}")
            
            # Test login with original password
            print(f"Testing login with original password...")
            if argon2.verify(original_password, user.password):
                print("✓ Original password works")
            else:
                print("✗ Original password doesn't work")
                return
            
            # Request password reset
            print("Requesting password reset...")
            await request_password_reset(test_email, db)
            print("✓ Password reset requested")
            
            # Get the reset token from database
            from app.db.models.password_reset_token import PasswordResetToken
            result = await db.execute(
                select(PasswordResetToken).where(
                    PasswordResetToken.user_id == user.id
                ).order_by(PasswordResetToken.created_at.desc()).limit(1)
            )
            reset_token = result.scalar_one_or_none()
            
            if not reset_token:
                print("✗ Reset token not found")
                return
            
            print(f"✓ Reset token found: {reset_token.token}")
            
            # Reset password
            new_password = "NewPassword456!"
            print(f"Resetting password to: {new_password}")
            await reset_password(reset_token.token, new_password, db)
            print("✓ Password reset completed")
            
            # Refresh user data
            await db.refresh(user)
            
            # Test login with new password
            print("Testing login with new password...")
            if argon2.verify(new_password, user.password):
                print("✓ New password works")
            else:
                print("✗ New password doesn't work")
                return
            
            # Test that old password no longer works
            print("Testing that old password no longer works...")
            if not argon2.verify(original_password, user.password):
                print("✓ Old password no longer works")
            else:
                print("✗ Old password still works (this is bad!)")
                return
            
            print("\n🎉 Password reset test completed successfully!")
            
        except Exception as e:
            print(f"✗ Error during test: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await db.close()

if __name__ == "__main__":
    asyncio.run(test_password_reset())
