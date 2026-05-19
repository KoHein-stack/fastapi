from fastapi import  FastAPI
from . import models
from .database import engine, get_db
# from sqlalchemy.orm import Session
from .router import auth, post, user, vote
from .config import settings
 
 

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
    
@app.get("/")
# Return a simple welcome message for the API root.
async def root():
    return {"message": "Hello, World!"}


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





# @app.get("/sqlalchemy")
# async def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts


# Find and return an in-memory post by id.
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p
#     return None

# # Find the index of an in-memory post by id.
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
#     return None

