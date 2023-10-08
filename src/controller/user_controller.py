from typing import Annotated

from fastapi import APIRouter, File
from fastapi.responses import StreamingResponse
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.models.models import (
    UserInCreation_Pydantic, 
    UserIn_Pydantic,
    UserInPicture_Pydantic, 
    Users
)

router = APIRouter()


@router.get(
    "/user/{username}",
    response_model=UserInPicture_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user(username: str, password: str):
    return await UserInPicture_Pydantic.from_queryset_single(
        Users.get(username=username, password=password)
    )
    
@router.get(
    "/users/username",
    responses={404: {"model": HTTPNotFoundError}},
)   
async def get_users_username():
    users = await Users.all()
    return [user.username for user in users]

@router.get(
    "/user/{username}/picture",
    response_class=StreamingResponse,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user_avatar(username: str):
    user = await UserIn_Pydantic.from_queryset_single(Users.get(username=username))

    return StreamingResponse(
        iter([user.picture]),
        media_type="application/octet-stream",
    )
    
@router.get(
    "/user/{username}/creation-date",
    response_model=UserInPicture_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_creation_date(username: str):
    return await UserInPicture_Pydantic.from_queryset_single(Users.get(username=username))
    
@router.post("/register", responses={404: {"model": HTTPNotFoundError}})
async def create_user(user: UserInCreation_Pydantic):
    await Users.create(
        **user.dict(exclude_unset=True, exclude_defaults=True, exclude_none=True)
    )

@router.put("/user/{user_name}", responses={404: {"model": HTTPNotFoundError}})
async def create_file(user_name: str, file: Annotated[bytes, File()]):
    await Users.filter(username=user_name).update(picture=file)

@router.patch("/user/{user_name}", responses={404: {"model": HTTPNotFoundError}})
async def update_user_connection_status(user_name: str, is_connected: bool):
    await Users.filter(username=user_name).update(is_connected=is_connected)
    
@router.patch(
    "/user/{user_name}/description", 
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_user_description(user_name: str, description: str):
    await Users.filter(username=user_name).update(description=description)