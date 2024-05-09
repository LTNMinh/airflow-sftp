from typing import Any

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from file_transfer_plugin.hooks.sftp_hook import CustomSTFPHook


class FileTransferOperator(BaseOperator):
    """
    File Transfer Custom Operator

    Transfer files from source SFTP server to target SFTP server

    """

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

        super(FileTransferOperator, self).__init__(*args, **kwargs)

        self.sftp_source = CustomSTFPHook(source_conn_id)
        self.sftp_target = CustomSTFPHook(target_conn_id)
        self.maximum_size_in_bytes = maximum_size_in_bytes
        self.folder_path = folder_path
        self.pattern_matching = pattern_matching

    def execute(self, context: dict):
        """
        Executes the operator

        Args:
            context (dict): Airflow context
        """

        diff_files = self._get_difference_files()
        self._transfer_files(diff_files)

    def _get_difference_files(self) -> list | list[str]:
        """
        Get the list of files from the source SFTP server

        Returns:
            list of difference files
        """

        if not self.sftp_source.path_exists(self.folder_path):
            self.log.info("No path found in the source folder")
            return []

        # TODO Problem when dir have very large number of small files
        files_attribute = self.sftp_source.describe_directory(self.folder_path)
        self.log.info(f"Files found in the source folder {files_attribute}")

        source_files = self.sftp_source.get_files_by_pattern(
            self.folder_path, self.pattern_matching
        )
        target_files = self.sftp_target.get_files_by_pattern(
            self.folder_path, self.pattern_matching
        )

        diff_files = list(set(source_files) - set(target_files))
        self.log.info(f"Differences files found in the source folder {diff_files}")

        # TODO Problem when dir have very large files
        # TODO To scale with other method
        self._check_file_size(diff_files, files_attribute)

        return diff_files

    def _check_file_size(
        self, files: list[str], files_attribute: dict[str, Any]
    ) -> None:
        """
        Validation size of files before transfer

        Args:
            files list[str]: List of files to check
            files_attribute dict[str, Any]: files attribute. including size, modified time, etc.
                    {
                        '.gitkeep': {'size': 0, 'type': 'file', 'modify': '20240504101853'},
                        'hello.txt': {'size': 71, 'type': 'file', 'modify': '20240505075017'}
                    }
        """

        for f in files:
            fbytes = files_attribute[f]["size"]
            if fbytes > self.maximum_size_in_bytes:
                self.log.warning(
                    f"File {f} is larger than {self.maximum_size_in_bytes} bytes. {files_attribute[f]}"
                )

        return

    def _transfer_files(self, files: list[str]) -> None:
        """
            Transfer file from source to target
        Args:
            files (list[str]): list of file to transfer
        """

        for f in files:
            with (
                self.sftp_source.open(f"{self.folder_path}/{f}", "r") as source_file,
                self.sftp_target.open(f"{self.folder_path}/{f}", "w") as target_file,
            ):
                while True:
                    source_line = source_file.readline()
                    self.log.info(source_line)
                    if len(source_line) == 0:
                        break
                    target_file.write(source_line)
