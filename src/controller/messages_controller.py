from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.models.models import (
    Messages, 
    MessagesIn_Pydantic,
    MessagesIn_low_data_Pydantic
)

router = APIRouter()


@router.post("/messages", responses={404: {"model": HTTPNotFoundError}})
async def create_message(message: MessagesIn_low_data_Pydantic):
    await Messages.create(
        **message.dict(exclude_unset=True, exclude_defaults=True, exclude_none=True)
    )

@router.get(
    "/messages",
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_message():
    messages = await Messages.all().order_by("created_at").values()
    return {"messages": messages}


@router.patch("/messages/{message_id}/reaction", responses={404: {"model": HTTPNotFoundError}})
async def patch_message_reaction(message_id: int, new_reaction_nb: str):
    await Messages.filter(message_id=message_id).update(reaction_nb=new_reaction_nb)

@router.patch("/messages/readed", responses={404: {"model": HTTPNotFoundError}})
async def patch_message_readed(sender: str, receiver: str, is_readed: bool):
    await Messages.filter(sender=sender, receiver=receiver).update(is_readed=is_readed)