from airflow.models import BaseOperator
from airflow.providers.sftp.hooks.sftp import SFTPHook
from airflow.utils.decorators import apply_defaults


class FileTransferOperator(BaseOperator):
    """
        File Transfer Custom Operator
    """

    @apply_defaults
    def __init__(self, source_conn_id,target_conn_id, *args, **kwargs):
        super(FileTransferOperator, self).__init__(*args, **kwargs)
        self.sftp_source = SFTPHook(source_conn_id)
        self.sftp_destination = SFTPHook(target_conn_id)

    def execute(self, context):
        """
        Executes the operator
        """

        self.log.info("Hello, Airflow!")
