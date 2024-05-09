from datetime import datetime

from airflow import DAG
from file_transfer_plugin import FileTransferOperator

dag = DAG(
    "file_transfer",
    description="File Transfer example",
    schedule_interval="0 12 * * *",
    start_date=datetime(2017, 3, 20),
    catchup=False,
)

with dag:
    my_file_transfer = FileTransferOperator(
        source_conn_id="my_source_sftp",
        target_conn_id="my_target_sftp",
        folder_path="upload/",
        pattern_matching="*",
        task_id="file_transfer",
    )

    my_file_transfer
