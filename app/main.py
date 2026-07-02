from fastapi import FastAPI
from app.routers.library import router

app = FastAPI(
    title="Library Management API",
    description="A RESTful CRUD API built using FastAPI",
    version="1.0.0"
)

app.include_router(router)