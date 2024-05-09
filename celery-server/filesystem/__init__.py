import re
from abc import ABC, abstractmethod

import paramiko


class FileSystemClient(ABC):
    @abstractmethod
    def __init__(self, uri):
        pass

    @abstractmethod
    def open(self, file_path, mode):
        pass


class SFTPClient(FileSystemClient):
    # Define the SSH URL pattern
    SSH_URL_PATTERN = r"sftp://([^:]+):([^@]+)@([^:]+):(\d+)"

    def __init__(self, uri) -> None:
        """
        Send SSH URI to connect to the server

        Args:
            ssh_uri (_type_): SSH URI
                ssh://username:password@hostname:port
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Parse the URL using regex
        pattern = re.match(self.SSH_URL_PATTERN, uri)

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


def file_system_factory(uri) -> FileSystemClient:
    protocol = uri.split("://")[0]
    match protocol:
        case "sftp":
            return SFTPClient(uri)
        case "s3":
            raise Exception("Unsupported protocol")
        case "gcs":
            raise Exception("Unsupported protocol")
        case _:
            raise Exception("Unsupported protocol")
