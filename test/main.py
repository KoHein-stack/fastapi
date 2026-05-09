from typing import Optional
from random import randrange
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}

            ]
    
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/create_post")
async def create_post(post: Post = Body(...)):
    print(post)
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"new_post": f"Title: {post_dict['title']} Content: {post_dict['content']} Published: {post_dict['published']} Rating: {post_dict['rating']}",
             "message": "Post created successfully!", "post": post_dict}

@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    return {"post_detail": post}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None


