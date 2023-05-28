"""Module for QuoteModels that represent quotes."""


class QuoteModel:
    """A class that represents a quote.

    A quote consists of a body and an author.
    """

    def __init__(self, body: str, author: str = 'unknown'):
        """Create a new `QuoteModel` instance.

        Args:
            body (str): The body of the quote.
            author (str, optional): The author of the quote.
                Defaults to 'unknown'.
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Return a string representation of this object.

        Returns:
            str: A computer-readable string representation of obj.
        """
        return f"{self.body}, {self.author}"
