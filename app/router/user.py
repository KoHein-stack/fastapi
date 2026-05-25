


from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import models, oauth2, utils
from ..database import get_db
from ..schema import User, UserCreate, UserOut
from sqlalchemy.exc import IntegrityError
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserCreate , db: Session = Depends(get_db)):
    user_data = user.model_dump()
    user_data["password"] = utils.hash_password(user.password)
    new_user = models.User(**user_data)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    db.refresh(new_user)
    return new_user 


@router.get("/{id}", response_model=UserOut)
async def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user

@router.get("/", response_model=list[UserOut])
async def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found")    
    return users


 
