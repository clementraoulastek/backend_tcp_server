from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import src.views.messages_view as messages_view
import src.views.user_view as user_view

app = FastAPI(title="API for messagerie TCP server")
app.include_router(user_view.router)
app.include_router(messages_view.router)

register_tortoise(
    app,
    db_url="sqlite://src/db/db.sqlite3",
    modules={"models": ["src.models.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

