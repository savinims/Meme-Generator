"""Module to manipulate base image of the meme and overlay text message."""
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import textwrap
import random
import logging


class MemeEngine:
    """
    The MemeEngine class handles the creation of memes.

    It resizes an image, adds text to it.
    It saves the resulting image to a specified directory.
    Attributes:
        output_dir (str): The directory to save meme images.
    """

    def __init__(self, output_dir: str) -> None:
        """
        Create a MemeEngine object instance.

        Args:
            output_dir (str): The directory to save meme images.
        """
        self.output_dir = output_dir

    def resize_image(self, original_image: Image, max_width: int) -> Image:
        """
        Resizes an image to have a max width while maintaining aspect ratio.

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

    def get_random_location(self, width, height, lb, ub):
        """
        Generate a random location within the specified bounds.

        Args:
            width (int): The width of the image.
            height (int): The height of the image.
            lb (float): Lower bound of the text location as a % of the
                image width or height.
            ub (float): Upper bound of the text location as a % of the
                image width or height.

        Returns:
            tuple: A tuple containing the coordinates (x, y).
        """
        x = random.uniform(width * lb, width * ub)
        y = random.uniform(height * lb, height * ub)
        return x, y

    def wrap_text(self, message, message_width, valid_width):
        """
        Wrap a message into multiple lines to fit within the valid_width.

        Args:
            message (str): The text message to be wrapped.
            message_width (int): Width of the original message in pixels.
            valid_width (int): Width of the available space in pixels.

        Returns:
            list: A list of wrapped lines, where each line fits within
                  the valid_width constraint.

        """
        avg_char_width = message_width / len(message)
        wrapped_width = int(valid_width / avg_char_width)
        wrapper = textwrap.TextWrapper(width=wrapped_width)
        wrapped_lines = wrapper.wrap(text=message)
        return wrapped_lines

    def overlay_text(
            self, resized_image: Image, text: str, author: str, font_path: str,
            font_size: int = 20, font_color: str = "white",
            lb: float = 0.01, ub: float = 0.5) -> None:
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
            font_color (str): The color to use for the text. Default "white".
            lb (float): Lower bound of the text location as a %
                of image width or height.
            ub (float): Upper bound of the text location as a %
                of image width or height.
        """
        draw = ImageDraw.Draw(resized_image)
        message = text + ' - ' + author
        font = ImageFont.truetype(font_path, size=font_size)

        x, y = self.get_random_location(
            width=resized_image.width, height=resized_image.height,
            lb=lb, ub=ub)
        message_width, message_height = font.getsize(message)
        if message_width > (resized_image.width - x - 3):
            wrapped_lines = self.wrap_text(
                message, message_width, (resized_image.width - x - 3))

            for i, line in enumerate(wrapped_lines):
                draw.text((x, y + message_height * i), line,
                          font=font, fill=font_color)
        else:
            draw.text((x, y), message, font=font, fill=font_color)

    def read_image(self, img_path):
        """
        Read an image from the specified path.

        Args:
            img_path (str): The path to the image file.

        Returns:
            PIL.Image.Image or None: The loaded image,
            or None if the file is not found or cannot be opened.
        """
        try:
            original_image = Image.open(img_path)
            return original_image
        except FileNotFoundError:
            logging.error("File not found")
            return None
        except Exception as e:
            logging.error(f"Error opening image: {str(e)}")
            return None

    def save_image(self, datestr_frmt, resized_image):
        """
        Save the resized image to the specified output directory.

        Args:
            datestr_frmt (str): The format string for the date to be
                used in the output filename.
            resized_image (PIL.Image.Image): The resized image
                as a PIL.Image.Image object.

        Returns:
            str or None: The filepath of the saved image if successful,
                or None if there was an error.
        """
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir)
            except OSError as e:
                logging.error(
                    f"Error creating directory: {self.output_dir}:\
                        {e.strerror}")
                return None

        output_filepath = os.path.join(
            self.output_dir, datetime.now().strftime(datestr_frmt) + '.jpg')
        try:
            resized_image.save(output_filepath)
            return output_filepath
        except IOError as e:
            logging.error(f"Error saving image: {e.strerror}")
            return None

    def make_meme(
            self, img_path: str, text: str, author: str,
            max_width: int = 500,
            font_path: str = "./_data/fonts/LilitaOne-Regular.ttf",
            datestr_frmt: str = "%m%d%Y_%H%M%S") -> str:
        """
        Create a meme.

        Resize the image at the specified path and add text to it.
        Save the resulting image to the specified directory.
        Args:
            img_path (str): Path to the image.
            text (str): The text to add to the image.
            author (str): The author of the meme.
            max_width (int): The max width of the resized image. Default 500.
            font_path (str): The path to the font file to use.
            datestr_frmt (str): The timestamp format to use in output file.
                Defaults to "%m%d%Y_%H%M%S".

        Returns:
            str: The path to the saved meme image.
        """
        original_image = self.read_image(img_path)

        resized_image = self.resize_image(original_image, max_width)
        self.overlay_text(resized_image, text, author, font_path)

        output_filepath = self.save_image(datestr_frmt, resized_image)

        return output_filepath
