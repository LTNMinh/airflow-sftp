import paramiko
from airflow.models import BaseOperator
from airflow.providers.sftp.hooks.sftp import SFTPHook
from airflow.utils.decorators import apply_defaults


class FileTransferOperator(BaseOperator):
    """
        File Transfer Custom Operator
    """

    @apply_defaults
    def __init__(self, source_conn_id,target_conn_id, folder_path,pattern_matching= "*",maximum_size_in_bytes = 1000, *args, **kwargs):
        super(FileTransferOperator, self).__init__(*args, **kwargs)
        self.sftp_source = SFTPHook(source_conn_id)
        self.sftp_target = SFTPHook(target_conn_id)
        self.maximum_size_in_bytes = maximum_size_in_bytes
        self.folder_path = folder_path
        self.pattern_matching = pattern_matching

    def execute(self, context):
        """
            Executes the operator
        """

        diff_files = self._get_difference_files()
        self._transfer_files(diff_files)

        self.log.info("Hello, Airflow!")

    def _get_difference_files(self):
        """
            Get the list of files from the source SFTP server
        """

        self.log.info("Getting list of files from source SFTP server")
        
        if (not self.sftp_source.path_exists(self.folder_path)):
            self.log.info("No path found in the source folder")
            return []

        #TODO Problem when dir have very large number of small files
        files_attribute = self.sftp_source.describe_directory(self.folder_path)
        self.log.info(f"Files found in the source folder {files_attribute}")
        
        
        source_files = self.sftp_source.get_files_by_pattern(self.folder_path,self.pattern_matching)
        target_files = self.sftp_target.get_files_by_pattern(self.folder_path,self.pattern_matching)

    
        diff_files = list(set(source_files) - set(target_files))
        self.log.info(f"Differences files found in the source folder {diff_files}")

        #TODO Problem when dir have very large files
        #TODO To scale with other method
        self._check_file_size(diff_files,files_attribute)

        return diff_files
    
    def _check_file_size(self, files,files_attribute):
        """
            Validation file size before transfer
        """

        for f in files:
            fbytes = files_attribute[f]['size']
            if fbytes > self.maximum_size_in_bytes:
                self.log.warning(f"File {f} is larger than {self.maximum_size_in_bytes} bytes. {files_attribute[f]}")
        
        return 
    
    def _transfer_files(self, files):
        """
            Transfer files from source to target
        """

        for f in files:
            source_conn: paramiko.SFTPClient = self.sftp_source.get_conn()
            target_conn: paramiko.SFTPClient = self.sftp_target.get_conn()

            with (source_conn.open(f"{self.folder_path}/{f}",'r') as source_file,
                target_conn.open(f"{self.folder_path}/{f}",'w') as target_file,
            ):
                while True:  
                    source_line = source_file.readline()
                    self.log.info(source_line)
                    if len(source_line) == 0:
                        break
                    target_file.write(source_line)
            pass
