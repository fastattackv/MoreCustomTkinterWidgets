import customtkinter as ctk


class AskDialog(ctk.CTkToplevel):
    def __init__(self, title: str, message: str, yes="yes", no="no", *args, **kwargs):
        """TopLevel widget already configured to ask true / false

        :param title: title of the toplevel widget
        :param message: message to show
        :param yes: text to show in the yes button, "yes" by default
        :param no: text to show in the no button, "no" by default
        :param args: args for ctk.CTkToplevel
        :param kwargs: kwargs for ctk.CTkToplevel
        """
        super().__init__(*args, **kwargs)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

        self.title(title)

        self.label = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=15))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=15)

        self.yes_button = ctk.CTkButton(self, text=yes, command=self.yes)
        self.yes_button.grid(row=1, column=0, padx=10, pady=15)

        self.no_button = ctk.CTkButton(self, text=no, command=self.no)
        self.no_button.grid(row=1, column=1, padx=10, pady=15)

        self.response = None

        self.bind("<Return>", self.yes)
        self.bind("<Escape>", self.no)

    def yes(self, event=None):
        self.response = True
        self.grab_release()
        self.destroy()

    def no(self, event=None):
        self.response = False
        self.grab_release()
        self.destroy()

    def get_response(self) -> bool | None:
        """ Waits until the dialog is closed and returns the response the user gave (True if yes was selected, False if
        no was selected, None if the user cancelled) """
        self.master.wait_window(self)
        return self.response


def askyesno(title: str, message: str) -> bool | None:
    """Shows a TopLevel widget to ask a question

    :param title: title of the dialog
    :param message: message in the dialog
    :return: True if the "Yes" button was clicked, False if the "No" button was clicked, None if the dialog was closed
    """
    dialog = AskDialog(title, message)
    return dialog.get_response()
