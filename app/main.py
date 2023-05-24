from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas
import psycopg2
from database import SessionLocal
from api import router
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

import time

'''middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
    Middleware(FastAPILimiter, key_func=lambda _: "user", rate_limit=10),
]
'''

app = FastAPI(docs_url='/')
app.include_router(router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




