from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Client(BaseModel):
    login: str
    password: str
    
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login/{login}")
def login(client: Client):
    return {"login": client.login, "password": client.password}