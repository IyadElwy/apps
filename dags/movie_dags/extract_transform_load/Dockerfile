FROM python:3.12-bookworm

RUN useradd -u 1000 -m appuser
USER appuser

RUN ["pip", "install", "requests", "python-dotenv", "loki-logger-handler", "pydantic"]

WORKDIR /app

COPY . /app

RUN mkdir ./appdata
RUN mkdir ./temp_data
