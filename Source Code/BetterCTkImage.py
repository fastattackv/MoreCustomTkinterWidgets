import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
import os


def draw_corners(image: Image.Image, rad: int) -> Image.Image:
    """ Draws corners on the given image """
    if rad > 0:
        image = image.copy()
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new('L', image.size, 255)
        w, h = image.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        image.putalpha(alpha)
        return image
    else:
        return image


class BetterCTkImage(ctk.CTkImage):
    def __init__(self,
                 light_image: Image.Image | str = None,
                 dark_image: Image.Image | str = None,
                 size: tuple[int, int] = (20, 20),

                 rounded_corner_radius=0):
        """Upgraded CTkImage class with more functionalities

        :param light_image: light image or path to light image file
        :param dark_image: dark image or path to light dark file
        :param size: size of the images
        :param rounded_corner_radius: radius of the rounding of the corners, 0 means no rounding
        """
        if type(light_image) is str:
            if os.path.isfile(light_image):
                light_image = Image.open(light_image)
            else:
                raise ValueError(f"Path to light image file is incorrect: {light_image}")
        if type(dark_image) is str:
            if os.path.isfile(dark_image):
                dark_image = Image.open(dark_image)
            else:
                raise ValueError(f"Path to dark image file is incorrect: {dark_image}")

        super().__init__(light_image, dark_image, size)
        # keys of the dicts self._scaled_light_photo_images and self._scaled_dark_photo_images:
        # ((size_x, size_y), rounded_corner_radius)

        if type(rounded_corner_radius) is int:
            if rounded_corner_radius > 0:
                self.rounded_corners_radius = rounded_corner_radius
            else:
                self.rounded_corners_radius = 0
        else:
            raise ValueError(f"Type of rounded_corner_radius should be int, not: {type(rounded_corner_radius)}")

    def _get_scaled_light_photo_image(self, scaled_size: tuple[int, int]) -> "ImageTk.PhotoImage":
        if (scaled_size, self.rounded_corners_radius) in self._scaled_light_photo_images:
            return self._scaled_light_photo_images[(scaled_size, self.rounded_corners_radius)]
        else:
            image = draw_corners(self._light_image, self.rounded_corners_radius)
            image = ImageTk.PhotoImage(image.resize(scaled_size))
            self._scaled_light_photo_images[(scaled_size, self.rounded_corners_radius)] = image
            return self._scaled_light_photo_images[(scaled_size, self.rounded_corners_radius)]

    def _get_scaled_dark_photo_image(self, scaled_size: tuple[int, int]) -> "ImageTk.PhotoImage":
        if (scaled_size, self.rounded_corners_radius) in self._scaled_dark_photo_images:
            return self._scaled_dark_photo_images[(scaled_size, self.rounded_corners_radius)]
        else:
            image = draw_corners(self._dark_image, self.rounded_corners_radius)
            image = ImageTk.PhotoImage(image.resize(scaled_size))
            self._scaled_dark_photo_images[(scaled_size, self.rounded_corners_radius)] = image
            return self._scaled_dark_photo_images[(scaled_size, self.rounded_corners_radius)]

    def configure(self, **kwargs):
        """ Changes the given arguments to the given values """
        if "rounded_corner_radius" in kwargs:
            value = kwargs.pop("rounded_corner_radius")
            if value > 0:
                self.rounded_corners_radius = value
            else:
                self.rounded_corners_radius = 0

        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        """ Returns the value of the given argument """
        if attribute_name == "rounded_corner_radius":
            return self.rounded_corners_radius
        else:
            return super().cget(attribute_name)
