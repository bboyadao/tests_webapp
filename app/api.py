import orjson
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import get_customer
from app.database import get_session
from app.settings import settings

redis = settings.redis
score_routers = APIRouter()


async def cache_user_data(user_id: str, data: dict):
    json_str = orjson.dumps(data, default=str)
    await redis.set(user_id, json_str)
    return {"stored_key": user_id}

async def get_user_cache(user_id: str):
    raw = await redis.get(user_id)
    if not raw:
        return None
    return orjson.loads(raw)


@score_routers.get("/get",)
async def scoring(
    customer_id: int,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
):
    data = await get_user_cache(customer_id)
    if data:
        return data

    customer = await get_customer(session, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    data = {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "credit_score": customer.credit_score,
        "explanation": customer.explanation
    }
    background_tasks.add_task(cache_user_data, customer_id, data)
    return data
