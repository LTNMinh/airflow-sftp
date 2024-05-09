from abc import ABC, abstractmethod

from airflow.hooks.base import BaseHook


class FileSystemHook(BaseHook, ABC):
    """
    Abstract class/Interface for file system hooks.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def open(self, file_path, mode):
        pass

    @abstractmethod
    def to_uri(self):
        pass

    @abstractmethod
    def path_exists(self, path):
        pass

    @abstractmethod
    def describe_directory(self, path):
        pass

    @abstractmethod
    def get_files_by_pattern(self, path, pattern_matching):
        pass
