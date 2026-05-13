from time import time
from typing import Optional
from random import randrange
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from starlette.responses import Response
from starlette import status
from psycopg2 import connect, OperationalError
import psycopg2
from psycopg2.extras import RealDictCursor
 

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except OperationalError as error:
        print("Connecting to database failed!")
        print("Error: ", error)
        time.sleep(2)

# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     print(posts)
#     conn.close()
#     print("Database connection was successful!")
# except Exception as error:
#     print("Connecting to database failed!")
#     print("Error: ", error)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}

            ]
    
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
async def get_posts():
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        print(posts)
        conn.close()
        return {"data": posts}
    except Exception as error:
        print("Error: ", error)

    return {"data": [dict(post) for post in my_posts]}

@app.post("/create_post", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post = Body(...)):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)
    return {"data": new_post}
    

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
    return None