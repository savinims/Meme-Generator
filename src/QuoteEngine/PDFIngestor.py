from typing import List
import subprocess
import os
import random
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    """
    A class for ingesting quotes from PDF files.
    """

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses a PDF file and returns a list of QuoteModel objects.

        Args:
            path (str): The path to the PDF file.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects representing the quotes in the file.

        Raises:
            Exception: If the file cannot be ingested.
        """

        if not cls.can_ingest(path):
            raise Exception('Cannot Ingest Exception')

        tmp = f'./tmp/{random.randint(0,1000000)}.txt'
        call = subprocess.call(['pdftotext', path, tmp])

        file_ref = open(tmp, "r")
        quotes = []
        for line in file_ref.readlines():
            line = line.strip('\n\r').strip()
            if len(line) > 0:
                parse_list = line.split('-')
                new_quote = QuoteModel(parse_list[0], parse_list[1])
                quotes.append(new_quote)

        file_ref.close()
        os.remove(tmp)

        return quotes
