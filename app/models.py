from .database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    content = Column(String, index=True, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(String, default="now()")


