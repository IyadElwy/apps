import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth


class CommandBody(BaseModel):
    command: str


class Movie(BaseModel):
    title: str


app = FastAPI()


@app.post("/cmd")
def cmd(command_body: CommandBody):
    res = requests.post(
        "http://portfolio-vm-1:5003/cmd",
        json={"command": command_body.command},
        headers={"Content-type": "application/json"},
    )
    res.raise_for_status()

    return res.json()


@app.post("/initdag")
def init_dag(movie: Movie):
    res = requests.post(
        "https://airflow.iyadelwy.xyz/api/v1/dags/movie_retriever_dag/dagRuns",
        headers={"Content-Type": "application/json"},
        json={"conf": {"title": movie.title}},
        auth=HTTPBasicAuth("iyadelwy", "airflow"),
    )
    res.raise_for_status()

    return res.json()


app.mount("/", StaticFiles(directory="../web", html=True), name="static")
