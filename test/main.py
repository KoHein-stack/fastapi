from typing import Optional
from random import randrange
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from starlette.responses import Response
from starlette import status

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}

            ]
    
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
async def get_posts():
    return {"data": my_posts}

@app.post("/create_post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post = Body(...)):
    print(post)
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"new_post": f"Title: {post_dict['title']} Content: {post_dict['content']} Published: {post_dict['published']} Rating: {post_dict['rating']}",
             "message": "Post created successfully!", "post": post_dict}

@app.get("/posts/latest")
async def get_latest_post():
    return {"latest_post": my_posts[-1] if my_posts else None}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post = Body(...)):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    my_posts[index] = post.dict()
    my_posts[index]['id'] = id
    return {"message": "Post updated successfully!", "post": my_posts[index]}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"Post with id: {id} not found"}
    return {"post_detail": post}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
