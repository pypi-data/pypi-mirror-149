import os
import glob
from typing import List
from zipfile import ZipFile
from contextlib import contextmanager
from .watchdog_utils import Handler, Watcher


class BotFilesPlugin:

    def get_all_file_paths(self, directory_path: str = None) -> List[str]:
        """
        Get the path of all files present in the given directory.

        Args:
            directory_path (str, optional): The directory to list the content. Defaults to current directory.

        Returns:
            List[str]: The list containing the path of all files present in the folder.
        """
        if not directory_path:
            directory_path = os.getcwd()

        file_paths = []
        for root, directories, files in os.walk(directory_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        return file_paths

    def zip_files(self, files_path: List[str], zip_filename: str) -> None:
        """
        Create a zip file containing all the given files.

        Args:
            files_path (List[str]): The list of files to be zipped.
            zip_filename (str): The path where the zip file will be saved.
        """
        if files_path:
            with ZipFile(zip_filename, "w") as zip:
                for file in files_path:
                    zip.write(file, os.path.basename(file))

    def zip_directory(self, directory_path: str, zip_filename: str) -> None:
        """
        Zip the given folder with all files and subfolders.

        Args:
            directory_path (str): The directory to be zipped.
            zip_filename (str): The path where the zip file will be saved.
        """
        file_paths = self.get_all_file_paths(directory_path)

        if file_paths:
            with ZipFile(zip_filename, "w") as zip:
                for file in file_paths:
                    zip.write(file)

    def unzip_all(self, zip_file: str, destination_folder: str = None) -> None:
        """
        Extract all content from a zip file.

        Args:
            zip_file (str): The path of the zip file to be extracted.
            destination_folder (str, optional): The folder where the zip file content will be saved.
                Defaults to current directory.
        """
        with ZipFile(zip_file, "r") as zip:
            zip.extractall(destination_folder)

    def unzip_file(self, zip_file: str, file_to_extract: str, destination_folder: str = None) -> None:
        """
        Extract a specified file from a zip file.

        Args:
            zip_file (str): The path of the zip file that contains the file to extract.
            file_to_extract (str): The name/path of the file that is in the zip file.
            destination_folder (str, optional): The folder where the extracted file will be saved.
                Defaults to current directory.
        """
        with ZipFile(zip_file, "r") as zip:
            zip.extract(file_to_extract, destination_folder)

    def get_last_created_file(self, directory_path: str = None, file_extension: str = "") -> str:
        """
        Returns the last created file in a specific folder.

        Args:
            directory_path (str, optional): The path of the folder where the file is expected.
                Defaults to current directory.
            file_extension (str, optional): The extension of the file to be searched for (e.g., .pdf, .txt).
                Defaults to any file.

        Returns:
            str: The path of the last created file.
        """
        if not directory_path:
            directory_path = os.getcwd()

        files_path = glob.glob(os.path.expanduser(os.path.join(directory_path, f"*{file_extension}")))
        if files_path:
            last_created_file = max(files_path, key=os.path.getctime)
            return last_created_file
        return ""

    @contextmanager
    def wait_for_file(self, directory_path: str = None, file_extension: str = "", timeout: int = 60000) -> None:
        """
        Wait for a new file to be available at the specified path until a timeout.

        Args:
            directory_path (str): The path of the folder where the file is expected.
                Defaults to the current working directory.
            file_extension (str, optional): The extension of the file to be searched for (e.g., .pdf, .txt).
                Defaults to any file.
            timeout (int, optional): Maximum wait time (ms) to wait for the file.
                Defaults to 60000ms (60s).

        Note:
            This method should be used as a context manager.
        """
        try:
            if not directory_path:
                directory_path = os.getcwd()

            watcher = Watcher(directory_path, timeout, Handler(file_extension))
            yield
        finally:
            watcher.run()
