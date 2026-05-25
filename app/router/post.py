
from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import oauth2
from .. import models, utils
from sqlalchemy import func
    
from ..database import get_db
from ..schema import Post, PostCreate, PostOut, PostUpdate
router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)




# @router.get("/", response_model=List[Post])
@router.get("/", response_model=List[PostOut])
# Fetch all posts from the database, with an in-memory fallback if the query fails.
async def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
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
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).add_columns(
            func.count(models.Vote.post_id).label("votes")
            ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return results



    # return {"data": [dict(post) for post in my_posts]}

@router.post("/create_post", status_code=status.HTTP_201_CREATED, response_model=Post)
# Create a new post in the database and return the inserted record.
async def create_post(post: PostCreate = Body(...), db: Session = Depends(get_db), 
                      current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(new_post)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@router.get("/latest")
# Return the most recent post from the in-memory posts list.
async def get_latest_post(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return  posts[-1] if posts else None

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
# Delete a post by id and return 404 if the post does not exist.
async def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete this post")    
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
async def update_post(id: int, updated_post: PostUpdate = Body(...), db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_query = db.query(models.Post).filter(models.Post.id == id)
    post = updated_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update this post")
    updated_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return  updated_query.first()



@router.get("/{id}", response_model=Post)
# Fetch one post by id from the database and return 404 if it is missing.
async def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to view this post")
    return post
    
