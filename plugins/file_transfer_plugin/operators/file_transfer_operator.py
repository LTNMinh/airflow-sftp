from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class FileTransferOperator(BaseOperator):
    """
        File Transfer Custom Operator
    """

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(FileTransferOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        """
        Executes the operator
        """
        self.log.info("Hello, Airflow!")
