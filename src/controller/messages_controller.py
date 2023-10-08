from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.expressions import Q

from src.models.models import (
    Messages, 
    Messages_Pydantic,
    MessagesIn_low_data_Pydantic
)

router = APIRouter()

room_list = ["home"]

@router.post("/messages", responses={404: {"model": HTTPNotFoundError}})
async def create_message(message: MessagesIn_low_data_Pydantic):
    message = await Messages.create(
        **message.dict(exclude_unset=True, exclude_defaults=True, exclude_none=True)
    )
    return message

@router.get(
    "/messages",
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_message(message_id: int, number: int, user1: str, user2: str):
    if room := next(
        (user for user in [user1, user2] if user in room_list), None
    ):
        messages = await Messages.filter(
            receiver=room, message_id__lt=message_id
        ).order_by("-message_id").limit(number).values()
    else:
        messages = await Messages.filter(
            Q(Q(sender=user1, receiver=user2), Q(sender=user2, receiver=user1), join_type=Q.OR), message_id__lt=message_id
        ).order_by("-message_id").limit(number).values()

    return {"messages": messages}

@router.get(
    "/messages/{message_id}",
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_message(message_id: int):
    message = await Messages.all().filter(message_id=message_id).values()
    return {"message": message}

@router.get(
    "/dm",
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user_dm(username: str):
    messages = await Messages.filter(
        Q(sender=username, receiver=username, join_type=Q.OR)
    ).values()

    usernames = list(
        {
            message["sender"]
            if message["sender"] != username
            else message["receiver"]
            for message in messages
        }
    )
    # TODO: add room endpoint to avoid this shit
    if "home" not in usernames:
        usernames.append("home")

    return {"usernames": usernames}

@router.get(
    "/last_id",
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_last_message_id():
    last_message = await Messages.all().order_by("-message_id").limit(1).values()

    return {"last_id" : last_message[0]["message_id"] if last_message else None}


@router.get(
    "/first_id",
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_first_message_id(user1: str, user2: str):
    first_message = await Messages.filter(
        Q(Q(sender=user1, receiver=user2), Q(sender=user2, receiver=user1), join_type=Q.OR)
        ).order_by("message_id").limit(1).values()
    
    return {"first_id" : first_message[0]["message_id"]}


@router.patch("/messages/{message_id}/reaction", responses={404: {"model": HTTPNotFoundError}})
async def patch_message_reaction(message_id: int, new_reaction_nb: str):
    await Messages.filter(message_id=message_id).update(reaction_nb=new_reaction_nb)

@router.patch("/messages/readed", responses={404: {"model": HTTPNotFoundError}})
async def patch_message_readed(sender: str, receiver: str, is_readed: bool):
    await Messages.filter(sender=sender, receiver=receiver).update(is_readed=is_readed)