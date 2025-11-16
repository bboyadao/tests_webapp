from fastapi import APIRouter
from app.api import score_routers


app_routers: APIRouter = APIRouter()
app_routers.include_router(score_routers, prefix="/scoring", tags=["SCORE"])
