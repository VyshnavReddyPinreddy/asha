from datetime import datetime,timedelta,timezone

from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel 
from sqlalchemy import text 
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import generate_otp,hash_password
from core.email import send_otp_email

import logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Password Reset"]
)

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    otp: str
    new_password: str

@router.post('/forgot-password')
async def forgot_password(payload:ForgotPasswordRequest,db:AsyncSession=Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT user_id,email 
             FROM user_account
             WHERE email = :email 
        """),
        {"email":payload.email}
    )

    user = result.mappings().first() 

    if not user : 
        raise HTTPException(404,"Email not found")
    
    otp = generate_otp()

    expiry = datetime.now(timezone.utc) + timedelta(minutes=10)

    await db.execute(
        text("""
        UPDATE user_account
        SET
            reset_otp = :otp,
            otp_expiry = :expiry
        WHERE user_id = :uid
        """),
        {
            "otp": otp,
            "expiry": expiry,
            "uid": user["user_id"]
        }
    )

    await db.commit()

    try:
        await send_otp_email(user["email"], otp)
        logger.info(f"OTP email sent to {user['email']}")
    except Exception as e:
        logger.error(f"Failed to send OTP email: {e}")
        raise HTTPException(500, f"Email send failed: {str(e)}")


    return {
        "message": "OTP sent successfully"
    }


@router.post("/reset-password")
async def reset_password(
    payload: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):

    if len(payload.new_password) < 8:
        raise HTTPException(
            400,
            "Password must be at least 8 characters long"
        )

    result = await db.execute(
        text("""
        SELECT user_id,
               reset_otp,
               otp_expiry
        FROM user_account
        WHERE email = :email
        """),
        {"email": payload.email}
    )

    user = result.mappings().first()

    if not user:
        raise HTTPException(
            404,
            "User not found"
        )

    if user["reset_otp"] != payload.otp:
        raise HTTPException(
            400,
            "Invalid OTP"
        )

    if datetime.now(timezone.utc) > user["otp_expiry"]:
        raise HTTPException(
            400,
            "OTP expired"
        )

    hashed_password = hash_password(
        payload.new_password
    )

    await db.execute(
        text("""
        UPDATE user_account
        SET
            password_hash = :password,
            reset_otp = NULL,
            otp_expiry = NULL
        WHERE user_id = :uid
        """),
        {
            "password": hashed_password,
            "uid": user["user_id"]
        }
    )

    await db.commit()

    return {
        "message": "Password updated successfully"
    }

