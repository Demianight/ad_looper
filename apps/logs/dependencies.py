from fastapi import Request


async def log_request_response(request: Request):
    response = await request.app.router.default(
        request.scope, request.receive, request.send
    )
    print("epic")
    return response
