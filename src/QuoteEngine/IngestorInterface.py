"""Module implementing the abstract base class based interface for ingesting different types of files."""
from abc import ABC, abstractmethod
from typing import List
from .QuoteModel import QuoteModel


class IngestorInterface(ABC):   
    """An abstract base class that defines the interface for ingesting different types of files containing quotes."""
    
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path):
        """
        Return True if the given file path has an allowed extension, False otherwise.

        Args:
            path (str): The file path to check.

        Returns:
            bool: True if the file can be ingested, False otherwise.
        """
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the file at the given path and returns a list of QuoteModel objects.

        This is an abstract method and must be implemented by any concrete subclass of
        IngestorInterface.

        Args:
            path (str): The file path to parse.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects parsed from the file.
        """
        pass
