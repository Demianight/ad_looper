from starlette.middleware.base import BaseHTTPMiddleware
from apps.auth.utils import decode_access_token
from apps.common.dependencies import get_db
from apps.logs import crud as logs_crud


from fastapi import Request, Response


from typing import Awaitable, Callable


class LogRequestResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ):
        response = await call_next(request)

        try:
            data = decode_access_token(
                request.headers["Authorization"].removeprefix("Bearer ")
            )
            display_device_id = data["display_device_id"]
            async for db in get_db():
                await logs_crud.create_log(
                    db,
                    url=request.url.path,
                    method=request.method,
                    status_code=response.status_code,
                    device_id=display_device_id,
                )
        except KeyError:
            pass

        return response
