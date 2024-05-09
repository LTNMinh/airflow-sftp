from airflow.plugins_manager import AirflowPlugin

from file_transfer_plugin.hooks.sftp_hook import CustomSTFPHook
from file_transfer_plugin.operators.celery_file_transfer_operator import (
    CeleryFileTransferOperator,
)
from file_transfer_plugin.operators.file_transfer_operator import FileTransferOperator


class FileTransferPlugin(AirflowPlugin):
    """
    Custom Airflow plugin to register custom operators, hooks, etc.
    """

    name = "file_transfer_plugin"

    hooks = [CustomSTFPHook]
    operators = [FileTransferOperator, CeleryFileTransferOperator]
