"""Module to manipulate base image of the meme and overlay text message."""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import textwrap
import random

class MemeEngine:
    """
    The MemeEngine class handles the creation of memes.

    It resizes an image, adds text to it,and saves the resulting image to a specified directory.
    Attributes:
        output_dir (str): The directory where the meme images will be saved.
    """

    def __init__(self, output_dir: str) -> None:
        """
        Create a MemeEngine object instance.

        Args:
            output_dir (str): The directory where the meme images will be saved.
        """
        self.output_dir = output_dir

    def resize_image(self, original_image: Image, max_width: int) -> Image:
        """
        Resizes an image to have a maximum width of `max_width` while maintaining its aspect ratio.

        Args:
            original_image (Image): The original image to resize.
            max_width (int): The maximum width of the resized image.

        Returns:
            Image: The resized image.
        """
        if original_image.width > max_width:
            ratio = max_width / original_image.width
            new_height = round(original_image.height * ratio)
            resized_image = original_image.resize((max_width, new_height))
        else:
            resized_image = original_image

        return resized_image

    def overlay_text(self, resized_image: Image, text: str, author: str,
                     font_path: str, font_size: int = 20, font_color: str = "white") -> None:
        """
        Overlay text on an image.

        Write text at a random location in the image.
        Wrap text that is wider than image width.

        Args:
            resized_image (Image): The image to overlay text on.
            text (str): The text to overlay.
            author (str): The author of the text.
            font_path (str): The path to the font file to use.
            font_size (int): The font size to use. Defaults to 20.
            font_color (str): The color to use for the text. Defaults to "white".
        """
        draw = ImageDraw.Draw(resized_image)
        message = text + ' - ' + author
        font = ImageFont.truetype(font_path, size=font_size)
        
        x = random.uniform( resized_image.width*0.01, resized_image.width*0.5)
        y = random.uniform( resized_image.height*0.01, resized_image.height*0.5)
        
        
        message_width, message_height =font.getsize(message) 
        if message_width > (resized_image.width-x):
            avg_char_width = message_width/len(message)
            wrapped_width = int((resized_image.width-x)/(avg_char_width))
            wrapper = textwrap.TextWrapper(width=wrapped_width) 
            wrapped_lines = wrapper.wrap(text=message)
        
            for i,line in enumerate(wrapped_lines): 
                draw.text((x, y + message_height*i), line, font=font, fill=font_color)
        else:
            draw.text((x, y), message, font=font, fill=font_color)



    def read_image(self,img_path):
        """
        Read an image from the specified path.
    
        Args:
            img_path (str): The path to the image file.
    
        Returns:
            PIL.Image.Image or None: The loaded image as a PIL.Image.Image object if successful,
            or None if the file is not found or cannot be opened.
        """
        try:
            original_image = Image.open(img_path)
            return original_image
        except FileNotFoundError:
            print("File not found")
            return None
        except Exception as e:
            print(f"Error opening image: {str(e)}")
            return None

    def save_image(self, datestr_frmt, resized_image):
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
            except OSError as e:
                print(f"Error: {self.output_dir} : {e.strerror}")
                return None

        output_filepath = self.output_dir + '/' + \
            datetime.now().strftime(datestr_frmt) + '.jpg'
        try:
            resized_image.save(output_filepath)
            return output_filepath
        except IOError as e:
            print(f"Error: {e.strerror}")
            return None

    def make_meme(self, img_path: str, text: str, author: str, max_width: int = 500,
                  font_path: str = "./_data/fonts/LilitaOne-Regular.ttf", datestr_frmt: str = "%m%d%Y_%H%M%S") -> str:
        """
        Create a meme.

        Resize the image at the specified path and add text to it.
        Save the resulting image to the specified directory.
        Args:
            img_path (str): The path to the image to use as the base of the meme.
            text (str): The text to add to the image.
            author (str): The author of the meme.
            max_width (int): The maximum width of the resized image. Defaults to 500.
            font_path (str): The path to the font file to use.
            datestr_frmt (str): The format string for the timestamp to use in the output filename.
                Defaults to "%m%d%Y_%H%M%S".

        Returns:
            str: The path to the saved meme image.
        """
        original_image = self.read_image(img_path)

        resized_image = self.resize_image(original_image, max_width)
        self.overlay_text(resized_image, text, author, font_path)

        output_filepath = self.save_image(datestr_frmt, resized_image)

        return output_filepath
