from airflow.providers.sftp.hooks.sftp import SFTPHook
from paramiko import SFTPFile


class CustomSTFPHook(SFTPHook):
    """Custome SFTP Hook inherited from airflow.providers.sftp.hooks.sftp.SFTPHook

    Expand read stream for SFTP


    Args:
        SFTPHook (_type_): _description_
    """

    def __init__(
        self,
        sftp_conn_id: str | None = "sftp_default",
        *args,
        **kwargs,
    ) -> None:
        super().__init__(ssh_conn_id=sftp_conn_id, *args, **kwargs)

    def open(self, f: str, mode: str = "r") -> SFTPFile:
        conn = self.get_conn()
        return conn.open(f, mode)
