from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TxtIngestor(IngestorInterface):
    """
    A class for ingesting quotes from .txt files.
    """

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses a .txt file and returns a list of QuoteModel objects.

        Args:
            path (str): The path to the .txt file.

        Returns:
            List[QuoteModel]: A list of QuoteModel objects representing the quotes in the file.

        Raises:
            Exception: If the file cannot be ingested.
        """

        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []
        with open(path, 'r') as f:
            for line in f:
                parts_list = line.split('-')
                new_quote = QuoteModel(parts_list[0], parts_list[1])
                quotes.append(new_quote)

        return quotes
