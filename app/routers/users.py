from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.get("/users/")
async def read_users():
    return [{"user.id":"IDEXAMPLE123"}]

@router.get("/users/{uid}")
async def read_user(uid:str):
    return {
        f"{uid}":"fake_uid",
        "fake":"fasle user"
    }
