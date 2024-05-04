from airflow.plugins_manager import AirflowPlugin
from file_transfer_plugin.operators.file_transfer_operator import \
    FileTransferOperator


class FileTransferPlugin(AirflowPlugin):
    """
    Custom Airflow plugin to register custom operators, hooks, etc.
    """
    name = "file_transfer_plugin"


    operators = [FileTransferOperator]

