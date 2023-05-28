"""Module implementing the ingestor logic."""
from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .DocxIngestor import DocxIngestor
from .CSVIngestor import CSVIngestor
from .PDFIngestor import PDFIngestor
from .TextIngestor import TextIngestor
import logging


class Ingestor(IngestorInterface):
    """
    Class for ingesting files and extracting quotes using importers.

    Attributes:
    importers (list): A list of importer classes that are used to ingest
    different types of files.
    """

    importers = [DocxIngestor, CSVIngestor, PDFIngestor, TextIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Ingest a file and extract quotes using appropriate importer.

        Parameters:
        path (str): The path to the file to be ingested.

        Returns:
        A list of QuoteModel objects extracted from the file.
        """
        ingested = False
        quotes = []

        for importer in cls.importers:
            if importer.can_ingest(path):
                quotes = importer.parse(path)
                ingested = True

        if not ingested:
            logging.error("Unsupported file ", path)

        return quotes
