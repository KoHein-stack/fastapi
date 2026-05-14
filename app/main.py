from time import time
from typing import Optional
from random import randrange
from fastapi import Depends, FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from starlette.responses import Response
from starlette import status
from psycopg2 import connect, OperationalError
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
import time
from sqlalchemy.orm import Session
from .schema import PostCreate, PostUpdate, Post
 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


    
@app.get("/")
# Return a simple welcome message for the API root.
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts", response_model=list[Post])
# Fetch all posts from the database, with an in-memory fallback if the query fails.
async def get_posts(db: Session = Depends(get_db)):
    # try:
    #     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password', cursor_factory=RealDictCursor)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM posts")
    #     posts = cursor.fetchall()
    #     print(posts)
    #     conn.close()
    #     return {"data": posts}
    # except Exception as error:
    #     print("Error: ", error)
    #     return {"data": my_posts}
    posts = db.query(models.Post).all()
    return posts



    # return {"data": [dict(post) for post in my_posts]}

@app.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=Post)
# Create a new post in the database and return the inserted record.
async def create_post(post: PostCreate = Body(...)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(new_post)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db = next(get_db()) # Get a database session from the generator function
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)

    return new_post
    

@app.get("/posts/latest")
# Return the most recent post from the in-memory posts list.
async def get_latest_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts[-1] if posts else None

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
# Delete a post by id and return 404 if the post does not exist.
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    db.delete(post, synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)                 
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if not deleted_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")      
   
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=Post)
# Update a database post by id and return the updated post.
async def update_post(id: int, updated_post: PostUpdate = Body(...), db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_query = db.query(models.Post).filter(models.Post.id == id)
    post = updated_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    updated_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    updated_post = updated_query.first()

    return updated_post


@app.get("/posts/{id}", response_model=Post)
# Fetch one post by id from the database and return 404 if it is missing.
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return post
    

@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# Find and return an in-memory post by id.
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None

# Find the index of an in-memory post by id.
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None
