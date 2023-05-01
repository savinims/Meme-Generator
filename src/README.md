# Meme Generator Project Overview

The Meme Generator is a multimedia application designed to dynamically generate memes, including an image with an overlaid quote. 
The application reads quotes from a variety of file formats and displays them on top of images. The project is packaged as a command-line tool and a simple 
web service. The webservice is able to create motivational modes in the 'Random' and 'Creator' modes.
In the random mode, a randomly selected image from the src/_data/photos/dog/ folder is overlayed with a random motivational quote from one of the files in src/_data/DogQuotes/.
In the creator mode, the user provides the URL of the base image, the motivational quote and its author.

The main parts of the project include
1) The QuoteEngine, which is resposible for extracting the motivational quotes and their authors from a variety of file formats.
2) The MemeEngine, which is responsible for generating the memes by overlaying the text of motivational quotes on a base image.
3) Command line interface, which takes several optional parameters.
4) Flask web app, which is able to create memes in both 'Random' and 'Creator' modes.

![Random Mode](src/Images/Random.JPG)
![Creator Mode](src/Images/Creator.JPG)

### Quote Engine

The Quote Engine module is responsible for ingesting different types of files that contain quotes. 
Each quote contains a body and an author. The system extracts each quote line-by-line from these files.
The IngestorInterface abstract base class defines two methods: `can_ingest(cls, path: str) -> boolean` and `parse(cls, path: str) -> List[QuoteModel]`. 
Separate strategy objects realize IngestorInterface for each file type (csv, docx, pdf, txt). 
The Ingestor class realizes the IngestorInterface abstract base class and encapsulates helper classes. 
It implements logic to select the appropriate helper for a given file based on the file type.

### Meme Engine

The Meme Engine Module is responsible for manipulating and drawing text onto images using the third-party Pillow library.
It resizes images to have a maximum with of 500 pixels. The font sizes are adjusted such that the motivational quotes fit within the base image.


### Command-Line Interface Tool
The utility can be run from the terminal by invoking `python3 meme.py`. 
The script takes three optional CLI arguments: `--body` a string quote body, `--author` a string quote author, and `--path` an image path. 
The script returns a path to a generated image. If any argument is not defined, a random selection is used.

### Flask Web Service
In the 'Random' mode, the app uses the Quote Engine Module and Meme Generator Modules to generate a random captioned image. 
In the 'Creator' mode, it uses the requests package to fetch an image from a user-submitted URL and overlays it with a user-submitted quote.

## Running the Code

Necessary dependencies for this project are included in the requirements.txt file. A user can replicate this work by recreating a virtual environment consisting of these dependencies.
The following commands can be used to run the Flask web-app

set FLASK_APP=app.py
flask run --host 0.0.0.0 --port 3000 --reload 

