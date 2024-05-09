from typing import Any

from airflow.utils.decorators import apply_defaults
from celery import Celery
from file_transfer_plugin.hooks.sftp_hook import CustomSTFPHook
from file_transfer_plugin.operators.file_transfer_operator import FileTransferOperator


class CeleryFileTransferOperator(FileTransferOperator):
    """
    File Transfer With Celery Backend Operator

    Call Celery Server to transfer files from source SFTP server to target SFTP server

    """

    list_tasks = [
        "tasks.transfer_file",
    ]

    @apply_defaults
    def __init__(
        self,
        source_conn_id: str,
        target_conn_id: str,
        folder_path: str,
        pattern_matching: str = "*",
        maximum_size_in_bytes: int = 1000,
        *args,
        **kwargs,
    ):
        """
            File transfer initialization

        Args:
            source_conn_id (str): source connection id provide by Airflow
            target_conn_id (str): target connection id provide by Airflow
            folder_path (str): folder path matching
            pattern_matching (str, optional): regex pattern to find a file. Defaults to "*".
            maximum_size_in_bytes (int, optional): maximum_size_in_bytes to loads from source to destination. Defaults to 1000.
        """

        super(CeleryFileTransferOperator, self).__init__(
            source_conn_id=source_conn_id,
            target_conn_id=target_conn_id,
            folder_path=folder_path,
            pattern_matching=pattern_matching,
            maximum_size_in_bytes=maximum_size_in_bytes,
            *args,
            **kwargs,
        )

        # TODO Expose to Celery Hook
        self.celery_client = Celery(
            "tasks", backend="redis://redis:6379/1", broker="redis://redis:6379/1"
        )

    def execute(self, context: dict):
        """
        Executes the operator

        Args:
            context (dict): Airflow context
        """

        diff_files = self._get_difference_files()

        # Call Celery Server to transfer files
        for file in diff_files:
            self.celery_client.send_task(
                "tasks.transfer_file",
                kwargs={
                    "source_uri": self.sftp_source.to_uri(),
                    "target_uri": self.sftp_target.to_uri(),
                    "file_path": f"{self.folder_path}/{file}",
                },
            )
