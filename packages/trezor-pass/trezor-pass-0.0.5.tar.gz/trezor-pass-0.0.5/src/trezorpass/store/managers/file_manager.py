from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from .manager import Manager

class FileManager(Manager):
    @property
    def password_store(self) -> bytes:
        filepath = inquirer.filepath(
            "Enter path to the password store file:",
            validate=PathValidator(is_file=True, message="Input is not a file")
        ).execute()
        with open(filepath, "rb") as file:
            return file.read()