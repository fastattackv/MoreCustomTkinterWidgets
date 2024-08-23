import customtkinter as ctk
from PIL import Image, ImageTk
import os
from typing import Tuple


class AnimatedImage(ctk.CTkImage):
    def __init__(self,
                 light_image: Image.Image | str = None,
                 dark_image: Image.Image | str = None,
                 size: Tuple[int, int] = (20, 20),
                 speed_multiplier=1.
                 ):
        """Image object functioning like CTkImage but allows to animate Images sequences (FLI/FLC, GIF)

        :param light_image: PIL.Image.Image (FLI/FLC or GIF format) or path to image for light mode
        :param dark_image: PIL.Image.Image (FLI/FLC or GIF format) or path to image for dark mode
        :param size: tuple (<width>, <height>) with display size for both images
        :param speed_multiplier: allows to change the speed of the animation: below 1 speeds the animation up and above 1 slows the animation down
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

        self._currently_animating = False
        self._time_between_frames = 0
        self._speed_multiplier = speed_multiplier
        self.reset_after_complete = False

        # New keys of the dicts self._scaled_light_photo_images and self._scaled_dark_photo_images:
        # ((size_x, size_y), frame_index)

    def _get_scaled_light_photo_image(self, scaled_size: Tuple[int, int]) -> "ImageTk.PhotoImage":
        if (scaled_size, self._light_image.tell()) in self._scaled_light_photo_images:
            return self._scaled_light_photo_images[(scaled_size, self._light_image.tell())]
        else:
            self._scaled_light_photo_images[(scaled_size, self._light_image.tell())] = ImageTk.PhotoImage(self._light_image.resize(scaled_size))
            return self._scaled_light_photo_images[(scaled_size, self._light_image.tell())]

    def _get_scaled_dark_photo_image(self, scaled_size: Tuple[int, int]) -> "ImageTk.PhotoImage":
        if (scaled_size, self._dark_image.tell()) in self._scaled_dark_photo_images:
            return self._scaled_dark_photo_images[(scaled_size, self._dark_image.tell())]
        else:
            self._scaled_dark_photo_images[(scaled_size, self._dark_image.tell())] = ImageTk.PhotoImage(self._dark_image.resize(scaled_size))
            return self._scaled_dark_photo_images[(scaled_size, self._dark_image.tell())]

    def configure(self, **kwargs):
        if "speed_multiplier" in kwargs:
            self._speed_multiplier = kwargs.pop("speed_multiplier")
            time_between_2_frames = self._light_image.info["duration"] if self._light_image is not None else self._dark_image.info["duration"]
            self._time_between_frames = int(time_between_2_frames * self._speed_multiplier)

        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if "speed_multiplier" == attribute_name:
            return self._speed_multiplier
        else:
            return super().cget(attribute_name)

    def _next_frame(self):
        """ Internal func: changes the current frame to the next one"""
        if self._currently_animating:
            try:  # light image
                if self._light_image is not None:
                    self._light_image.seek(self._light_image.tell() + 1)
            except EOFError:
                self._light_image.seek(0)

            try:  # dark image
                if self._dark_image is not None:
                    self._dark_image.seek(self._dark_image.tell() + 1)
            except EOFError:
                self._dark_image.seek(0)

            for callback in self._configure_callback_list:
                callback()

            self._configure_callback_list[0].__self__.after(self._time_between_frames, self._next_frame)

    def get_animation_state(self) -> bool:
        """Returns information about the animation

        :return: True if the animation is on over, False otherwise
        """
        return self._currently_animating

    def start_animation(self):
        """ Starts the animation loop """
        self._currently_animating = True
        time_between_2_frames = self._light_image.info["duration"] if self._light_image is not None else self._dark_image.info["duration"]
        self._time_between_frames = int(time_between_2_frames * self._speed_multiplier)
        self._next_frame()

    def stop_animation(self):
        """ Stops the animation loop """
        if self._currently_animating:
            self._currently_animating = False
            if self.reset_after_complete:
                self.set_to_frame(0)
                self.reset_after_complete = False
        else:
            raise RuntimeError("Tried to stop the animation but it was not already running")

    def start_animation_for(self, ms: int, reset_after_complete=False):
        """Starts the animation and stops automatically after the given time

        :param ms: time to run the animation for (in ms)
        :param reset_after_complete: if set to True: resets to the first frame of the animation when the animation stops
        """
        try:
            self._configure_callback_list[0].__self__.after(ms, self.stop_animation)
        except AttributeError:
            pass
        else:
            self.start_animation()
            self.reset_after_complete = reset_after_complete

    def set_to_frame(self, frame_index: int):
        """Sets the animation to the given frame

        :param frame_index: frame index to set the animation to (1st frame is index 0)
        """
        if self._light_image is not None:
            self._light_image.seek(frame_index)
        if self._dark_image is not None:
            self._dark_image.seek(frame_index)
        for callback in self._configure_callback_list:
            callback()
