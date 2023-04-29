# Meme Generator Project Overview

The Meme Generator project is a multimedia application designed to dynamically generate memes, including an image with an overlaid quote. The application reads quotes from a variety of file formats and displays them on top of images.

## Quote Engine

The Quote Engine module is responsible for ingesting many types of files that contain quotes. Each quote contains a body and an author. The system extracts each quote line-by-line from these files.
The IngestorInterface abstract base class defines two methods: `can_ingest(cls, path: str) -> boolean` and `parse(cls, path: str) -> List[QuoteModel]`. Separate strategy objects realize IngestorInterface for each file type (csv, docx, pdf, txt). The Ingestor class realizes the IngestorInterface abstract base class and encapsulates helper classes. It implements logic to select the appropriate helper for a given file based on the file type.

## Meme Engine

The Meme Engine Module is responsible for manipulating and drawing text onto images using the third-party Pillow library

## The Application

The Meme Generator project is packaged as a command-line tool and a simple web service.

### Command-Line Interface Tool
The utility can be run from the terminal by invoking `python3 meme.py`. The script takes three optional CLI arguments: `--body` a string quote body, `--author` a string quote author, and `--path` an image path. The script returns a path to a generated image. If any argument is not defined, a random selection is used.

### Flask Web Service
The app uses the Quote Engine Module and Meme Generator Modules to generate a random captioned image. It uses the requests package to fetch an image from a user-submitted URL. 
