from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os


class MemeEngine:
    """
    The MemeEngine class handles the creation of memes by resizing an image, adding text to it,
    and saving the resulting image to a specified directory.

    Attributes:
        output_dir (str): The directory where the meme images will be saved.
    """

    def __init__(self, output_dir: str):
        """
        Constructor for the MemeEngine class.

        Args:
            output_dir (str): The directory where the meme images will be saved.
        """
        self.output_dir = output_dir

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500, font_path: str = "./_data/fonts/LilitaOne-Regular.ttf", datestr_frmt: str = "%m%d%Y_%H%M%S") -> str:
        """
        Creates a meme by resizing the image at the specified path, adding text to it, and saving
        the resulting image to the specified directory.

        Args:
            img_path (str): The path to the image to use as the base of the meme.
            text (str): The text to add to the image.
            author (str): The author of the meme.
            width (int): The maximum width of the resized image. Defaults to 500.
            font_path (str): The path to the font file to use.
            datestr_frmt (str): The format string for the timestamp to use in the output filename.
                Defaults to "%m%d%Y_%H%M%S".

        Returns:
            str: The path to the saved meme image.
        """

        original_image = Image.open(img_path)

        if original_image.width > width:
            ratio = width / original_image.width
            new_height = round(original_image.height * ratio)
            resized_image = original_image.resize((width, new_height))
        else:
            resized_image = original_image

        draw = ImageDraw.Draw(resized_image)
        
        message = text +'-'+author       
        font = ImageFont.truetype(font_path, size=20)

        text_width, text_height = draw.textsize(message, font=font)
        x = (resized_image.width - text_width) / 2
        y = (resized_image.height - text_height) / 2
        draw.text((x, y), message, font=font, fill="white")
     
        
        if not os.path.exists(self.output_dir):
           os.makedirs(self.output_dir)

        output_filepath = self.output_dir + '/' + \
            datetime.now().strftime(datestr_frmt) + '.jpg'
        resized_image.save(output_filepath)

        return output_filepath
