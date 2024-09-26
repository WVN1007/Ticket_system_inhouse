from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from app.oauth_utils import oauth2_scheme
from typing import Annotated
import app.schemas as schemas

router = APIRouter(tags=['Authentication'],prefix="/api")

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/login')
@router.post("/login", response_model=schemas.Token)
async def login(formdata: Annotated[OAuth2PasswordRequestForm,Depends()]):
    # lookup the user from the formdata
    print(formdata)
    access_token = "access"
    return {"access_token": access_token, "token_type": "bearer"}
