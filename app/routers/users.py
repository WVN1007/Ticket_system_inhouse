"""Router to Users data"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.get("/users/")
async def read_users():
    '''Get all users, NOTE: ADMIN only'''
    return [{"user.id":"IDEXAMPLE123"}]

@router.get("/users/me")
async def read_current_user():
    '''Get current logged in user'''
    return {"myuid":"my fakeuid"}

@router.get("/users/{uid}")
async def read_user(uid:str):
    return {
        f"{uid}":"fake_uid",
        "fake":"fasle user"
    }
