import re

import celeryconfig
import paramiko
from celery import Celery

app = Celery(__name__)
app.config_from_object(celeryconfig)


class SFTPClient:
    # Define the SSH URL pattern
    SSH_URL_PATTERN = r"ssh://([^:]+):([^@]+)@([^:]+):(\d+)"

    def __init__(self, ssh_uri) -> None:
        """
        Send SSH URI to connect to the server

        Args:
            ssh_uri (_type_): SSH URI
                ssh://username:password@hostname:port
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Parse the URL using regex
        pattern = re.match(self.SSH_URL_PATTERN, ssh_uri)

        if pattern:
            username = pattern.group(1)
            password = pattern.group(2)
            hostname = pattern.group(3)
            port = pattern.group(4)

            client.connect(hostname, port=port, username=username, password=password)
            self.client = client.open_sftp()
        else:
            raise Exception("Can not parse SSH URI")

    def open(self, file_path, mode) -> paramiko.SFTPFile:
        return self.client.open(file_path, mode)


@app.task
def transfer_file(
    source_uri,
    target_uri,
    file_path,
):
    sftp_source = SFTPClient(source_uri)
    sftp_target = SFTPClient(target_uri)

    with (
        sftp_source.open(file_path, "r") as source_file,
        sftp_target.open(file_path, "w") as target_file,
    ):
        while True:
            source_line = source_file.readline()
            if len(source_line) == 0:
                break
            target_file.write(source_line)

    print("Transfer file")


if __name__ == "__main__":
    app.start()
