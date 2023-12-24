"""Entry point of the application."""

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.controller import messages_controller, user_controller

app = FastAPI(title="API for messagerie TCP server")
app.include_router(user_controller.router)
app.include_router(messages_controller.router)

register_tortoise(
    app,
    db_url="sqlite://src/db/db.sqlite3",
    modules={"models": ["src.models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
