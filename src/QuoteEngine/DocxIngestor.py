"""A concrete class for DOCX files."""
from typing import List
import docx
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class DocxIngestor(IngestorInterface):
    """A class implementing IngestorInterface for .docx files."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse a .docx file at a given path and return a list of QuoteModels.

        Args:
            path (str): The path to the .docx file to be ingested.

        Raises:
            Exception: If the file at the given path has an extension
            that is not allowed by this class.

        Returns:
            A list of QuoteModel objects parsed from the .docx file.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []

        doc = docx.Document(path)

        for para in doc.paragraphs:
            if para.text != "":
                parse_list = para.text.split('-')
                new_quote = QuoteModel(parse_list[0], parse_list[1])
                quotes.append(new_quote)

        return quotes
