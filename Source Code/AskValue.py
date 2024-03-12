import customtkinter as ctk
from typing import Literal

from Message import showwarning


class AskValue(ctk.CTkInputDialog):
    def __init__(self, typ: Literal["str", "int", "float"], allow_none=True, *args, **kwargs):
        """Modified instance of CTkInputDialog, allows verifying entered values

        :param typ: type of the value to enter, should be "str", "int" or "float"
        :param allow_none: if set to False, the user will not be allowed to enter "" (only useful for entering str type)
        :param args: args for CTkInputDialog
        :param kwargs: kwargs for CTkInputDialog
        """
        super().__init__(*args, **kwargs)
        self.type = typ
        self.allow_none = allow_none

    # overrides _ok_event method to add verification
    def _ok_event(self, event=None):
        value = self._entry.get()
        if self.type == "str":
            if not self.allow_none and value == "":
                showwarning("Entering value", "Enter a value")
            else:  # data is verified
                self._user_input = value
                self.grab_release()
                self.destroy()
        elif self.type == "int":
            if not value.isnumeric():
                showwarning("Entering value", "Enter an integer")
            else:  # data is verified
                self._user_input = value
                self.grab_release()
                self.destroy()
        elif self.type == "float":
            try:
                value = float(value)
            except ValueError:
                showwarning("Entering value", "Enter a decimal number")
            else:  # data is verified
                self._user_input = value
                self.grab_release()
                self.destroy()
        else:
            self._user_input = value
            self.grab_release()
            self.destroy()


def askstring(title: str, message: str, allow_none=True) -> str:
    """Asks a string from the user

    :param title: title of the TopLevel window
    :param message: message to show in the TopLevel window
    :param allow_none: optional: if set to False, the user will not be able to enter ""
    :return: string entered by the user, None if the user canceled
    """
    dialog = AskValue("str", allow_none, title=title, text=message)
    return dialog.get_input()


def askinteger(title: str, message: str) -> int:
    """Asks an int from the user

    :param title: title of the TopLevel window
    :param message: message to show in the TopLevel window
    :return: int entered by the user, None if the user canceled
    """
    dialog = AskValue("int", title=title, text=message)
    return dialog.get_input()


def askfloat(title: str, message: str) -> float:
    """Asks a string from the user

    :param title: title of the TopLevel window
    :param message: message to show in the TopLevel window
    :return: int entered by the user, None if the user canceled
    """
    dialog = AskValue("float", title=title, text=message)
    return dialog.get_input()
