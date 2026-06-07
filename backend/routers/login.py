from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text 
from core.database import get_db 
from core.security import verify_password,create_access_token

router = APIRouter(
    prefix="/auth",
    tags=['Login']
)

class LoginRequest(BaseModel):
    username : str
    password : str 
    
@router.post('/login')
async def login(payload: LoginRequest,db:AsyncSession=Depends(get_db)):
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

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"],
        "username": user["username"]
    }
    