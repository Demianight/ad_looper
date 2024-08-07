from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from .middleware import LogRequestResponseMiddleware
import apps


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(LogRequestResponseMiddleware)

app.include_router(apps.core_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
