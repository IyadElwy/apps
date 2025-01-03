import subprocess

from fastapi import FastAPI
from pydantic import BaseModel


class CommandBody(BaseModel):
    command: str


app = FastAPI()


@app.post("/cmd")
async def cmd(command_body: CommandBody):
    if "cd" in command_body.command:
        return {"result": "Sorry, you can't change the directory :)"}
    try:
        result = subprocess.run(command_body.command, capture_output=True, shell=True)
        encoded_result = result.stdout.decode("utf-8") + result.stderr.decode("utf-8")
        return {"result": encoded_result}
    except Exception:
        raise {"result": "Network Error: Your command did not reach the host machine."}
