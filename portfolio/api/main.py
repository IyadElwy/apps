from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.post("/cmd")
async def cmd():
    return {"result": "Yoo"}


app.mount("/", StaticFiles(directory="../web", html=True), name="static")
