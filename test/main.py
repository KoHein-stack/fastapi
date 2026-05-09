from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}]
    
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
async def get_posts():
    return {"data": "Here are your posts!"}

@app.post("/create_post")
async def create_post(post: Post = Body(...)):
    print(post)
    print(post.dict())
    return {"new_post": f"Title: {post.title} Content: {post.content} Published: {post.published} Rating: {post.rating}",
             "message": "Post created successfully!", "post": post}

