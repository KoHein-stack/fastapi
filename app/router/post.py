
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import models, utils
    
from ..database import get_db
from ..schema import Post, PostCreate, PostUpdate
router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)




@router.get("/", response_model=List[Post])
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

@router.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=Post)
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
    

@router.get("/latest")
# Return the most recent post from the in-memory posts list.
async def get_latest_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts[-1] if posts else None

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
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

@router.put("/{id}", response_model=Post)
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


@router.get("/{id}", response_model=Post)
# Fetch one post by id from the database and return 404 if it is missing.
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return post
    
