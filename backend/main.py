from fastapi import FastAPI
from routers.login import router as login_router
from routers.password_reset import router as password_reset_router
from routers.chat import router as chat_router

app = FastAPI(title="ASHA")

app.include_router(login_router)
app.include_router(password_reset_router)
app.include_router(chat_router)

