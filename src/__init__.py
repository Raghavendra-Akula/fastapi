from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.errors import UserAlreadyExists, InvalidToken
from src.errors import create_exception_handler
from fastapi.exceptions import HTTPException

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting .....")
    await init_db()
    yield
    print(f"server is stopped")
    return


version = "v1"

app = FastAPI(
    title="Bookly",
    description="FastAPI code for a book review web service",
    version= version,
)

app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message" : "Token is invalid or expired",
            "error_code" : "Token is editted or invalid",
            "resolution" : "Please refresh the token"
        }
    )
)

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message" : "User is already registered no need to register again",
            "error_code" : "user already exits",
            "resolution" : "Please follow another endpoint to enter has an existing user"
        }
    )
)

@app.exception_handler(500)
async def internal_server_error(request, exc):
    return JSONResponse(
        content= {
            "message" : "Oops something went wrong",
            "error_code" : "Server error"
        },
        status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])