FROM python:3.12-bookworm

RUN ["pip", "install", "fastapi[standard]", "pandas", "requests"]

WORKDIR /app

COPY ./api ./api

RUN ["mkdir", "/appdata"]

WORKDIR /appdata

COPY ./movies_command_line_app.py .

COPY ./movies.sh /bin/movies

RUN ["chmod", "+x", "/bin/movies"]

WORKDIR /app/api

ENTRYPOINT ["python3", "/app/api/run.py"]

RUN ["useradd", "-m", "-d", "/home/narrator", "narrator"]

USER narrator:narrator

WORKDIR /home/narrator
