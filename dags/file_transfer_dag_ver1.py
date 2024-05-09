from datetime import datetime

from airflow import DAG
from file_transfer_plugin import FileTransferOperator

dag = DAG(
    "file_transfe_ver_1",
    description="File Transfer Version 1",
    schedule_interval="0 1 * * *",
    start_date=datetime(2024, 3, 1),
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
