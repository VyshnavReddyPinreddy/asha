from fastapi import FastAPI
from routers.login import router as login_router
from routers.password_reset import router as password_reset_router
from routers.chat import router as chat_router
from routers.voice_query import router as voice_query_router
from routers.favorites import router as favorites_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ASHA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(password_reset_router)
app.include_router(chat_router)
app.include_router(voice_query_router)
app.include_router(favorites_router)

