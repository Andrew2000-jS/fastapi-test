from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.mongo import MongoDB
from app.database.redis import RedisManager
from app.routes.auth import auth_router
from app.routes.user import user_router
from app.routes.company import company_router
from app.conf.settings import settings
from app.exceptions.handlers import register_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect_db(settings.mongo_db_uri)
    await RedisManager.connect()
    try:
        yield
    finally:
        await MongoDB.disconnect_db()
        await RedisManager.close()
    
app = FastAPI(lifespan=lifespan, version="v1")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(company_router)