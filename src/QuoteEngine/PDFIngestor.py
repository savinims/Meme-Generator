"""A concrete class for PDF files."""
from typing import List
import subprocess
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    """A class for ingesting quotes from PDF files."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse a PDF file and returns a list of QuoteModel objects.

        Args:
            path (str): The path to the PDF file.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects representing the quotes in the file.

        Raises:
            Exception: If the file cannot be ingested.
        """
        if not cls.can_ingest(path):
            raise Exception('Cannot Ingest Exception')

        p = subprocess.Popen(
            ['pdftotext', '-layout', path, '-'], stdout=subprocess.PIPE)
        quotes = []
        for line in p.stdout:
            line = line.decode('utf-8').strip()

            if len(line) > 0:
                body, author = line.split('-')
                quotes.append(QuoteModel(body, author))

        return quotes
