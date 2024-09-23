from fastapi import APIRouter

router = APIRouter(
    prefix="/api/devs",
    tags=["devs"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
async def read_devs():
    '''Get all devs, NOTE: ADMIN only'''
    return [{"dev.id":"IDEXAMPLE123"}]

@router.get("/{uid}")
async def read_dev(uid:str):
    return {
        f"{uid}":"fake_uid",
        "fake":"fasle devs"
    }
