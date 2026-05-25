
from fastapi import APIRouter

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, schema, database, rate_limit
from ..database import get_db
from .. import oauth2


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schema.Token)
def login(
    request: Request,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    client_host = request.client.host if request.client else "unknown"
    limiter_key = f"{client_host}:{user_credentials.username.lower()}"

    rate_limit.check_login_rate_limit(limiter_key)

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user or not utils.verify_password(user_credentials.password, user.password):
        rate_limit.record_failed_login(limiter_key)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    rate_limit.clear_login_rate_limit(limiter_key)

    return {"access_token": access_token, "token_type": "bearer"}
