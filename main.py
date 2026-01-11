from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/greet")
async def greet(name: str = "User", age: int = 0) -> dict:
    return {"message": f"Hello, {name}!", "age" : age}

class BookCreateModal(BaseModel):
    author: str
    title : str


@app.post("/create_book")
async def create_book(book_data: BookCreateModal):
    return{
        "author": book_data.author,
        "title": book_data.title
    }


@app.get("/headers",status_code=201)
async def get_headers(accept: str = Header(None),
                      content_type: str = Header(None),
                      user_agent: str = Header(None),
                      host: str = Header(None)
                      ):
    Request_Headers = {}
    Request_Headers["accept"] = accept
    Request_Headers["content-type"] = content_type
    Request_Headers["user_agent"] = user_agent
    Request_Headers["host"] = host

    return Request_Headers