import asyncio
import os
import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Customer

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

fake = Faker()

# Một số explanation mẫu
EXPLANATION_POOL = [
    "High e-commerce spending history (Shopee, Tiki)",
    "Stable income transactions detected",
    "Positive social engagement (Twitter, Facebook)",
    "Frequent online shopping",
    "No late payments in last 12 months",
    "High follower engagement on social media",
]


async def create_mock_customers(total=100000, batch_size=1000):
    async with engine.begin() as conn:
        # Tạo bảng nếu chưa có
        await conn.run_sync(Base.metadata.create_all)

    session = AsyncSessionLocal()

    try:
        for i in range(0, total, batch_size):
            batch = []
            for _ in range(batch_size):
                name = fake.name()
                email = fake.unique.email()
                score = random.uniform(500, 850)
                explanation = random.sample(EXPLANATION_POOL, 3)
                customer = Customer(name=name, email=email, credit_score=score, explanation=explanation)
                batch.append(customer)

            session.add_all(batch)
            await session.commit()
            print(f"Inserted {i + batch_size} / {total} records")

    finally:
        await session.close()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_mock_customers())
