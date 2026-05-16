from time import time
from typing import Optional
from random import randrange
from fastapi import Depends, FastAPI, HTTPException
from fastapi.params import Body
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.responses import Response
from starlette import status
from psycopg2 import connect, OperationalError
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, utils
from .database import engine, get_db
import time
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .schema import PostCreate, PostUpdate, Post, UserCreate, UserOut
from .schema import User, UserCreate
from .router import auth, post, user
 
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
    
@app.get("/")
# Return a simple welcome message for the API root.
async def root():
    return {"message": "Hello, World!"}



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

