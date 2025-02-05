import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s

with DAG(
    dag_id="movie_retriever_dag",
    start_date=datetime.datetime(2025, 1, 4),
):
    extraction_pod = KubernetesPodOperator(
        task_id="movie-extract-transform-load",
        namespace="portfolio",
        image="iyadelwy/movie-extract_transform_load-image:latest",
        name="movie-extract-transform-load-pod",
        cmds=[
            "python",
            "./extract_transform_load.py",
        ],
        arguments=[
            "-t \"{{ dag_run.conf['title'] }}\"",
        ],
        volume_mounts=[
            k8s.V1VolumeMount(
                name="movie_processing_temp_volume", mount_path="/app/temp_data"
            )
        ],
        volumes=[
            k8s.V1Volume(
                name="movie_processing_temp_volume",
                persistent_volume_claim=k8s.V1PersistentVolumeClaim(
                    metadata=k8s.V1ObjectMeta(name="movie_processing_temp_pvc"),
                    spec=k8s.V1PersistentVolumeClaimSpec(
                        access_modes=["ReadWriteOnce"],
                        resources=k8s.V1ResourceRequirements(requests="100Mi"),
                        storage_class_name="longhorn",
                        volume_name="movie_processing_temp_volume",
                    ),
                ),
            ),
        ],
    )

    extraction_pod
