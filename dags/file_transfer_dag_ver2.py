from datetime import datetime

from airflow import DAG
from file_transfer_plugin import CeleryFileTransferOperator


def print_hello():
    from celery import Celery
    from celery.result import allow_join_result

    app = Celery("tasks", backend="redis://redis:6379/1", broker="redis://redis:6379/1")

    with allow_join_result():
        return app.send_task("tasks.transfer_file", args=[2, 2]).get()


dag = DAG(
    "file_transfer_ver_2",
    description="File Transfer Version 2",
    schedule_interval="0 1 * * *",
    start_date=datetime(2024, 3, 1),
    catchup=False,
)

with dag:
    my_file_transfer = CeleryFileTransferOperator(
        source_conn_id="my_source_sftp",
        target_conn_id="my_target_sftp",
        folder_path="upload/",
        pattern_matching="*",
        task_id="file_transfer",
    )

    my_file_transfer
