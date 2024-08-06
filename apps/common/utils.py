import asyncio
from typing import Sequence

from database.models import Base


async def load_awaitable_attrs(obj: Base | Sequence[Base], *attrs):
    if isinstance(obj, Base):
        obj = [obj]
    tasks = []
    for obj in obj:
        for attr in attrs:
            tasks.append(getattr(obj, attr))

    await asyncio.gather(*tasks)
