from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from src.tools.picture import return_default_pic


class Users(models.Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True)
    password = fields.CharField(max_length=30)
    picture = fields.BinaryField(default=return_default_pic)
    is_connected = fields.BooleanField(default=False)


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
UserInPicture_Pydantic = pydantic_model_creator(
    Users, name="UserInPicture", exclude_readonly=True, exclude=["picture"]
)

class Messages(models.Model):
    message_id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    sender = fields.CharField(max_length=30)
    receiver = fields.CharField(max_length=30)
    message = fields.TextField()
    is_readed = fields.BooleanField(default=False)
    reaction_nb = fields.IntField(default=0)


Messages_Pydantic = pydantic_model_creator(Messages, name="Message")
MessagesIn_Pydantic = pydantic_model_creator(
    Messages, name="MessageIn", exclude_readonly=True
)
MessagesIn_low_data_Pydantic = pydantic_model_creator(
    Messages, name="MessageInReaction", exclude_readonly=True, exclude=["reaction_nb", "is_readed"]
)
