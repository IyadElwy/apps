import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker_swarm import DockerOperator
from docker.types import Mount

with DAG(
    dag_id="movie_cleaner_dag",
    start_date=datetime.datetime(2025, 1, 12),
    schedule="0 9 * * *",
):
    clean_up_temp_directory = DockerOperator(
        task_id="clean-up-temp-directory",
        image="alpine:latest",
        command=("sh -c 'mkdir -p /app/temp_data && rm -rf /app/temp_data/*'"),
        user="1000",
        mount_tmp_dir=False,
        mounts=[
            Mount(
                target="/app/temp_data",
                source="/mnt/storage-server0/sda3/airflow/tmp",
                type="bind",
            ),
        ],
        auto_remove=True,
    )

    clean_up_temp_directory
