from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import time
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

logger = logging.getLogger('uvicorn.access')
logger.disabled = True


def register_middleware(app: FastAPI):
    
    @app.middleware(middleware_type='http')
    async def custom_logging(request: Request, call_next): #call_next for what route endpoint to be called or any other middle ware to be called post execution from this middleware.
        start_time = time.time()

        response = await call_next(Request)

        processing_time = time.time()-start_time
        message = f"{request.client.host} - {request.client.port} - {request.method} - {request.url.path} - {response.status_code} - completed after {processing_time}s"
        print(message)
        return response
    
    @app.middleware(middleware_type='http')# we are using decorator here because this middleware is a custom function we are adding this to our fastapi application. This is called on everyrequest which is reaching the server.
    async def Authorization(request: Request, call_next):
        if not "Authorization" in request.headers:
            return JSONResponse(
                content={
                    "message" : "Not Authenticated",
                    "resolution" : "Please provide tokens in required headers format"
                },
                status_code= status.HTTP_401_UNAUTHORIZED
            )
        response = await call_next(request)

        return response
    
    # This is a class based middleware. FastAPI wraps over this middleware when you are using existing class based middleware.
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials = True,
        )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts= ["localhost", "127.0.0.1"],
        www_redirect = True,
    )



