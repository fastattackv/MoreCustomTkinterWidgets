import customtkinter as ctk
import winsound
from PIL import Image
from typing import Literal


class Message(ctk.CTkToplevel):
    def __init__(self, title: str, message: str, typ: Literal["info", "warning", "error"], sound=True, *args, **kwargs):
        """TopLevel widget already configured for displaying messages

        :param title: title of the toplevel widget
        :param message: message to show
        :param typ: type of message to show ("info" / "warning" / "error")
        :param sound: optional: if set to True (True by default), the beep windows sound will be played as the message
            shows
        :param args: args for ctk.CTkToplevel
        :param kwargs: kwargs for ctk.CTkToplevel
        """
        super().__init__(*args, **kwargs)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

        self.title(title)

        if typ == "info":
            pil_image = Image.open("Images/info.png")
            ctk_image = ctk.CTkImage(pil_image, pil_image, (85, 85))
            self.image = ctk.CTkLabel(self, text="", image=ctk_image, width=85, height=85)
            self.image.grid(row=0, column=0, padx=10, pady=15)
            pil_image.close()
        elif typ == "warning":
            pil_image = Image.open("Images/warning.png")
            ctk_image = ctk.CTkImage(pil_image, pil_image, (85, 85))
            self.image = ctk.CTkLabel(self, text="", image=ctk_image, width=85, height=85)
            self.image.grid(row=0, column=0, padx=10, pady=15)
            pil_image.close()
        elif typ == "error":
            pil_image = Image.open("Images/error.png")
            ctk_image = ctk.CTkImage(pil_image, pil_image, (85, 85))
            self.image = ctk.CTkLabel(self, text="", image=ctk_image, width=85, height=85)
            self.image.grid(row=0, column=0, padx=10, pady=15)
            pil_image.close()

        self.label = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=15))
        self.label.grid(row=0, column=1, padx=10, pady=15)

        self.ok_button = ctk.CTkButton(self, text="Ok", command=self.ok)
        self.ok_button.grid(row=1, column=0, columnspan=2, padx=10, pady=15)

        if sound:
            if typ == "error":
                winsound.MessageBeep(16)
            else:
                winsound.MessageBeep()

        self.bind("<Return>", self.ok)

    def ok(self, event=None):
        self.grab_release()
        self.destroy()

    def wait_end(self):
        """ When called, waits until the message is closed """
        self.master.wait_window(self)


def showinfo(title: str, message: str):
    """Shows a TopLevel widget to tell an information

    :param title: title of the dialog
    :param message: message in the dialog
    """
    m = Message(title, message, "info")
    m.wait_end()


def showwarning(title: str, message: str):
    """Shows a TopLevel widget to tell a warning

    :param title: title of the dialog
    :param message: message in the dialog
    """
    m = Message(title, message, "warning")
    m.wait_end()


def showerror(title: str, message: str):
    """Shows a TopLevel widget to tell an error

    :param title: title of the dialog
    :param message: message in the dialog
    """
    m = Message(title, message, "error")
    m.wait_end()
