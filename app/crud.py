from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Customer


async def get_customer(session: AsyncSession, customer_id: int):
    result = await session.execute(select(Customer).where(Customer.id == customer_id))
    return result.scalar_one_or_none()
