from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.models.models import Messages, MessagesIn_Pydantic

router = APIRouter()


@router.post("/messages", responses={404: {"model": HTTPNotFoundError}})
async def create_message(message: MessagesIn_Pydantic):
    await Messages.create(**message.dict(exclude_unset=True))


@router.get(
    "/messages",
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_message():
    messages = await Messages.all().order_by("message_id").limit(20).values()
    return {"messages": messages}
