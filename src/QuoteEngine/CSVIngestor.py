"""A concrete class for CSV files."""
from typing import List
import pandas
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class CSVIngestor(IngestorInterface):
    """A class that ingests CSV files that contain quotes and returns a list of `QuoteModel` objects."""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a CSV file and returns a list of `QuoteModel` objects.

        This method is required by the `IngestorInterface` and must be implemented by all concrete
        subclasses. It reads in the CSV file at the given `path`, creates a new `QuoteModel` instance
        for each row in the file, and returns a list of all the `QuoteModel` instances created.

        Args:
            path (str): The file path of the CSV file to parse.

        Returns:
            List[QuoteModel]: A list of `QuoteModel` instances representing the quotes in the CSV file.
        """
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')

        quotes = []
        df = pandas.read_csv(path, header=0)

        for index, row in df.iterrows():
            new_quotes = QuoteModel(row['body'], row['author'])
            quotes.append(new_quotes)

        return quotes
