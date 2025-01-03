FROM python:3.12-bookworm

RUN ["pip", "install", "fastapi[standard]"]

WORKDIR /app

COPY . .

WORKDIR /app/api

ENTRYPOINT ["python3", "/app/api/run.py"]

RUN ["useradd", "-m", "-d", "/home/narrator", "narrator"]

USER narrator:narrator

WORKDIR /home/narrator
