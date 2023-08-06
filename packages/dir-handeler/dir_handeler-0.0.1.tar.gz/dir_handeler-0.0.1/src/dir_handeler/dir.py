# For typing.
from __future__ import annotations
from typing import Union

# For handeling filesystems.
from os import makedirs, path, unlink, listdir
from shutil import rmtree


class Dir:
    """Class to handle directory."""

    def __init__(self, name: str, parent: Union[str, Dir] = ""):
        """Initialize directory.

        Args:
            name (str): Directory name.
            parent (Union[str, Dir], optional): Parent directory as Directory or as path string. Defaults to "".
        """

        # Generate filepath.
        self.path = path.join(
            parent.path if isinstance(parent, Dir) else parent,
            name,
        )

        # Create directories.
        makedirs(self.path, exist_ok=True)

    def clear(self) -> Dir:
        """Clear directory.

        Returns:
            Dir: Itself.
        """
        for filename in listdir(self.path):
            file_path = self.file_path(filename)
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                rmtree(file_path)
        if listdir(self.path):
            raise Exception("Not all files where deleted!")
        return self

    def file_path(self, filename: str) -> str:
        """Generate filepath.

        Args:
            filename (str): Filename

        Returns:
            str: Filepath.
        """

        return path.join(self.path, filename)
