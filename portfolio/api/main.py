import logging
import time

import requests
from cachetools import TTLCache
from dotenv import dotenv_values
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth

config = dotenv_values(".env")


logger = logging.getLogger("web-api-logger")
logger.setLevel(logging.DEBUG)
custom_logging_handler = LokiLoggerHandler(
    url="http://loki:3100/loki/api/v1/push",
    labels={"application": "portfolio", "component": "web-api"},
)
logger.addHandler(custom_logging_handler)


class CommandBody(BaseModel):
    command: str


class Movie(BaseModel):
    title: str


app = FastAPI()
cache = TTLCache(maxsize=15, ttl=180)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    client_ip = request.client.host
    method = request.method
    path = request.url.path
    query_params = dict(request.query_params)
    user_agent = request.headers.get("user-agent", "unknown")
    try:
        body = await request.body()
        body = body.decode("utf-8") if body else "empty"
    except Exception:
        body = "Body could not be parsed"

    response = await call_next(request)

    response_time = time.time() - start_time
    status_code = response.status_code

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    log_string = f"[{timestamp}] | Method: {method} | Path: {path} | Query Params: {query_params} | Body: {body} | Client IP: {client_ip} | User-Agent: {user_agent} | Status Code: {status_code} | Response Time: {response_time:.2f}s"
    logging.info(log_string)

    return response


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
    cache_result = cache.get(movie.title)
    if cache_result:
        return {"result": "movie request is already being processed"}
    cache[movie.title] = "processing"
    res = requests.post(
        "https://airflow.iyadelwy.xyz/api/v1/dags/movie_retriever_dag/dagRuns",
        headers={"Content-Type": "application/json"},
        json={"conf": {"title": movie.title}},
        auth=HTTPBasicAuth(config["AIRFLOW_USER"], config["AIRFLOW_PASSWORD"]),
    )
    res.raise_for_status()

    return res.json()


app.mount("/", StaticFiles(directory="../web", html=True), name="static")
