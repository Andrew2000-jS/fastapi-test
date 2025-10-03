from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.mongo import MongoDB
from app.routes.auth import auth_router
from app.routes.user import user_router
from app.routes.company import company_router
from app.conf.consts import MONGO_DB_URI
from app.exceptions.handlers import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect_db(MONGO_DB_URI)
    try:
        yield
    finally:
        await MongoDB.disconnect_db()
    
app = FastAPI(lifespan=lifespan, version="v1")

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(company_router)