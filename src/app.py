"""Flask application for meme generation in Random and Creator modes."""
import random
import os
import requests
from flask import Flask, render_template, request
from MemeEngine import MemeEngine
from QuoteEngine.Ingestor import Ingestor
import tempfile

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """Load all resources.

    Returns:
    tuple: A tuple containing two lists, quotes and imgs.
    quotes contains all the quotes parsed from various files,
    and imgs contains the paths of all images in the _data/photos/dog/.
    """
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme in the 'Random' mode.

    Returns:
        str: HTML template with a randomly generated meme.
    """
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information.

    Returns:
        str: HTML template with a form for users to input information.
    """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user-defined meme in the 'Creator' mode.

    Returns:
        str: HTML template with a user-defined meme.
        In case of exception, returns the meme_form.
    """
    image_url = request.form.get("image_url")
    body = request.form.get("body")
    author = request.form.get("author")

    try:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            response = requests.get(image_url)
            response.raise_for_status()
            f.write(response.content)

        path = meme.make_meme(f.name, body, author)
        os.remove(f.name)
        return render_template('meme.html', path=path)

    except requests.exceptions.HTTPError as e:
        print(f"An error occurred in downloading the image: {str(e)}")
        return render_template('meme_form.html')
    except Exception as e:
        print(f"Failed to create meme: {str(e)}")
        return render_template('meme_form.html')


if __name__ == "__main__":
    """Flask app for meme generation."""
    app.run()
