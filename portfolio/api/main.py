import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


class CommandBody(BaseModel):
    command: str


app = FastAPI()


@app.post("/cmd")
async def cmd(command_body: CommandBody):
    res = requests.post(
        "http://portfolio-vm-1:5003/cmd",
        json={"command": command_body.command},
        headers={"Content-type": "application/json"},
    )
    res.raise_for_status()

    return res.json()


app.mount("/", StaticFiles(directory="../web", html=True), name="static")
