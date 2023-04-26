class QuoteModel:
    """A class that represents a quote. 

    A quote consists of a body and an author."""

    def __init__(self, body: str, author: str = 'unknown'):
        """Creates a new `QuoteModel` instance.

        Args:
            body (str): The body of the quote.
            author (str, optional): The author of the quote. Defaults to 'unknown'.
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Returns a string representation of this object that can be used to recreate it.

        Returns:
            str: A computer-readable string representation of this object.
        """
        return f"{self.body}, {self.author}"
