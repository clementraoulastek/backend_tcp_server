from typing import Annotated

from fastapi import FastAPI, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from src.models import (User_Pydantic, UserIn_Pydantic, UserInPicture_Pydantic,
                        Users)

app = FastAPI(title="API for messagerie TCP server")


class Status(BaseModel):
    message: str


@app.get(
    "/user/{username}",
    response_model=UserInPicture_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user(username: str, password: str):
    return await UserInPicture_Pydantic.from_queryset_single(
        Users.get(username=username, password=password)
    )


@app.get(
    "/user/{username}/picture",
    response_class=StreamingResponse,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user(username: str):
    test = await UserIn_Pydantic.from_queryset_single(Users.get(username=username))

    return StreamingResponse(
        iter([test.picture]),
        media_type="application/octet-stream",
    )


@app.post("/register", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.put("/user/{user_name}", responses={404: {"model": HTTPNotFoundError}})
async def create_file(user_name: str, file: Annotated[bytes, File()]):
    await Users.filter(username=user_name).update(picture=file)


register_tortoise(
    app,
    db_url="sqlite://src/db/db.sqlite3",
    modules={"models": ["src.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
