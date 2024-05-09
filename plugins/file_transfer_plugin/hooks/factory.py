from airflow.models.connection import Connection
from hooks import FileSystemHook
from hooks.sftp_hook import CustomSTFPHook


def file_system_hook_factory(conn_id) -> FileSystemHook:
    conn = Connection.get_connection_from_secrets(conn_id)

    match conn.conn_type:
        case "sftp":
            return CustomSTFPHook()
        case "s3":
            raise Exception("Unsupported protocol")
        case "gcs":
            raise Exception("Unsupported protocol")
        case _:
            raise Exception("Unsupported protocol")
