from fastapi import APIRouter
from app.api.v2.endpoints import health

api_router_v2 = APIRouter()
api_router_v2.include_router(health.router)