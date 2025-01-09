FROM python:3.12-bookworm

RUN ["pip", "install", "fastapi[standard]", "requests", "cachetools", "python-dotenv"]

WORKDIR /app

COPY . .

WORKDIR /app/api

ENTRYPOINT ["python3", "run.py"]

EXPOSE 5003
