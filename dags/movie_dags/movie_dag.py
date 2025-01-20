import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker_swarm import DockerOperator
from docker.types import Mount

with DAG(
    dag_id="movie_retriever_dag",
    start_date=datetime.datetime(2025, 1, 4),
):
    extraction_container = DockerOperator(
        task_id="movie-extract_transform_load",
        image="iyadelwy/movie-extract_transform_load-image:latest",
        command="python ./extract_transform_load.py -t \"{{ dag_run.conf['title'] }}\"",
        mount_tmp_dir=False,
        mounts=[
            Mount(
                target="/app/temp_data",
                source="/mnt/storage-server0/sda3/airflow/tmp",
                type="bind",
            ),
            Mount(
                target="/app/appdata/db.sqlite",
                source="/mnt/storage-server0/sda3/portfolio/data/db.sqlite",
                type="bind",
            ),
        ],
        auto_remove=True,
    )

    extraction_container
