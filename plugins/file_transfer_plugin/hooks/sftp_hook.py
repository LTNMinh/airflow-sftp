from typing import Any

from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook


class SFTPHook(BaseHook):

    conn_name_attr = "sftp_conn_id"
    default_conn_name = "sftp_conn_default"
    conn_type = "SFTP"
    hook_name = "SFTP Connection"


    def __init__(self, 
                conn_id = default_conn_name,
                   *args, 
                   **kwargs
                ):
        """
        Initializes hook for SFTP connection.
        """
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.connection = self.get_conn()

    def get_conn(self):
        """
        Initializes Connection for SFTP.
        """
        return self.get_connection(self.conn_id)