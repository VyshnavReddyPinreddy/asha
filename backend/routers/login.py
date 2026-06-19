from fastapi import APIRouter,Depends,HTTPException,status,Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text 
from core.database import get_db 
from core.security import verify_password,create_access_token
from core.security import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=['Login']
)

class LoginRequest(BaseModel):
    username : str
    password : str 
    
@router.post('/login')

async def login(payload: LoginRequest,response:Response,db:AsyncSession=Depends(get_db)):
    query = text("""
        SELECT user_id, username, password_hash, role, asha_id, anm_id 
        FROM user_account 
        WHERE username = :username
    """)

    result = await db.execute(query,{"username":payload.username})
    user = result.mappings().first()

    if not user or not verify_password(payload.password,user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    token_data = {
        "user_id": user["user_id"],
        "username": user["username"],
        "role": user["role"],
        "asha_id": user["asha_id"],
        "anm_id": user["anm_id"]
    }

    access_token = create_access_token(data=token_data)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,     # True in production HTTPS
        samesite="none",
        max_age=60 * 60 * 24
    )
    return {
        "message": "Login successful",
        "role": user["role"],
        "username": user["username"]
    }
    
@router.post("/logout")
async def logout(response: Response):

    response.delete_cookie(
        key="access_token"
    )

    return {
        "message": "Logged out"
    }

@router.get("/me")
async def me(
    current_user: dict = Depends(get_current_user)
):
    return {
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "role": current_user["role"]
    }