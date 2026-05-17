import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.database import get_db
from account.schemas import UserLoginSchema, UserRegisterSchema, UserRefreshTokenSchema
from account.models import UserModel, TokenModel
from auth.jwt_auth import generate_access_token, generate_refresh_token, decode_refresh_token

router = APIRouter(tags=["users"], prefix="/users")

def generate_tokens(length=32):
    return secrets.token_urlsafe(length)

@router.post("/login")
async def login(request: UserLoginSchema, db:Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username.lower()).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#    if not user_obj.verify_password(request.password):
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

#    token_obj = TokenModel(user_id=user_obj.id, token=generate_tokens())
#    db.add(token_obj)
#    db.commit()
#    db.refresh(token_obj)

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse(content={"detail": "user logged in", "access_token": access_token,
                                 "refresh_token": refresh_token},
                        status_code=status.HTTP_200_OK)

@router.post("/register")
async def register(request: UserRegisterSchema, db:Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    user_obj = UserModel(
        username=request.username.lower(),
    )
    db.add(user_obj)
    db.commit()
    return JSONResponse(content="user registered", status_code=status.HTTP_201_CREATED)


@router.post("/refresh_token")
async def user_refresh_token(request: UserRefreshTokenSchema, db:Session = Depends(get_db)):
    user_id = decode_refresh_token(request.token)
    access_token = generate_access_token(user_id)
    return JSONResponse(content={"access_token": access_token,})