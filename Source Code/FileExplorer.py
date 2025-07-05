"""
This file contains custom messagebox / simpledialog for the APY! launcher
"""

import customtkinter as ctk
import os
from PIL import Image
from typing import Literal, Optional, Union, Tuple

from .Message import showwarning
from .AskValue import askstring


def join_paths(path: str, *paths: str) -> str:
    """Joins the given paths and returns the joined path

    :param path: first path to join
    :param paths: other paths to add
    :return: final path
    """
    return os.path.join(path, *paths).replace("\\", "/")


class FileExplorer(ctk.CTkFrame):
    def __init__(self,
                 master: any,
                 responsetype: Literal["file", "directory"],

                 # file explorer parameters
                 filetypes: list[str] = None,
                 initialdir: str = None,
                 initialfile: str = None,

                 # customtkinter frame parameters
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 overwrite_preferred_drawing_method: Union[str, None] = None,
                 **kwargs):
        """File explorer widget to select a path that already contains scrollbars, see ctk.CTkFrame for widget arguments

        :param responsetype: type of the path to select ("file" / "directory")
        :param filetypes: extensions of the files that can be selected (ex: [".txt", ".csv"]), None if a directory should be selected or if all files can be selected
        :param initialdir: directory to start the selection from, if both initialdir and initialfile are None, the initialdir will be os.getcwd()
        :param initialfile: path of the file selected at the start of the search
        """
        # checking arguments
        if responsetype not in ["file", "directory"]:
            raise ValueError(f"responsetype should be \"file\" or \"directory\", not {responsetype}")
        if initialdir is not None and initialfile is not None:
            raise ValueError(f"Cannot use initialdir and initialfile at the same time, please set only one")
        if initialdir is not None and not os.path.isdir(initialdir):
            raise ValueError(f"Path of initialdir is unknown: {initialdir}")
        if initialfile is not None:
            if responsetype != "file":
                raise ValueError("Cannot use initialfile is responsetype is directory")
            if not os.path.isfile(initialfile):
                raise ValueError(f"Path of initialfile is unknown: {initialfile}")
            if filetypes is not None and initialfile.split(".")[-1] not in filetypes:
                raise ValueError(f"initialfile extension is not in filetypes: {initialfile.split(".")[-1]}")

        # creating widget
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color,
                         background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.response_type = responsetype
        self.filetypes = filetypes
        self.change_path = True  # if set to false, the tracing on self.selected_path will be disabled

        if initialdir is not None:
            self.path_to_show = ctk.StringVar(self, value=initialdir)  # always a directory, path to show in the explorer
            self.selected_path = ctk.StringVar(self, value=initialdir)  # selected path by the user
        elif initialfile is not None:
            self.path_to_show = ctk.StringVar(self, value=os.path.dirname(initialfile))
            self.selected_path = ctk.StringVar(self, value=initialfile)
        else:
            self.path_to_show = ctk.StringVar(self, value=os.getcwd())
            self.selected_path = ctk.StringVar(self, value=os.getcwd())
        self.selected_path.trace_add("write", self._user_path_changed)

        self.folder_image = ctk.CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "Images/folder_light.png")), Image.open(os.path.join(os.path.dirname(__file__), "Images/folder_dark.png")))
        self.file_image = ctk.CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "Images/file_light.png")), Image.open(os.path.join(os.path.dirname(__file__), "Images/file_dark.png")))

        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        if fg_color == "transparent":
            self.canvas.configure(bg=self._apply_appearance_mode(self.cget("bg")))
        else:
            self.canvas.configure(bg=self._apply_appearance_mode(self.cget("fg_color")))

        self.explorer_frame = ctk.CTkFrame(self.canvas, fg_color=fg_color)

        self.back_button = ctk.CTkButton(self, image=ctk.CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "Images/back_arrow_light.png")), Image.open(os.path.join(os.path.dirname(__file__), "Images/back_arrow_dark.png"))), text="", command=self._move_back, width=35)
        self.path_entry = ctk.CTkEntry(self, textvariable=self.selected_path)
        self.create_dir_button = ctk.CTkButton(self, image=ctk.CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "Images/new_folder_light.png")), Image.open(os.path.join(os.path.dirname(__file__), "Images/new_folder_dark.png"))), text="", command=self._create_directory, width=35)
        self.y_scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview)
        self.x_scrollbar = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)
        self.after(100, lambda: self.canvas.configure(xscrollcommand=self.x_scrollbar.set))  # you have to bind the other scrollbar at least 50ms after the first one, idk why but it works

        self.back_button.grid(row=0, column=0, padx=3, pady=3, sticky="nw")
        self.path_entry.grid(row=0, column=1, padx=3, pady=3, sticky="new")
        self.create_dir_button.grid(row=0, column=2, columnspan=2, padx=3, pady=3, sticky="ne")
        self.canvas.grid(row=1, column=0, columnspan=3, padx=3, pady=3, sticky="nsew")
        self.y_scrollbar.grid(row=1, column=3, rowspan=2, sticky="nse")
        self.x_scrollbar.grid(row=2, column=0, columnspan=3, sticky="sew")

        self.canvas.create_window((1, 1), window=self.explorer_frame, anchor="nw")

        self.explorer_frame.bind("<Configure>", self._configure_frame)
        self.canvas.bind("<MouseWheel>", self._mousewheel)
        self.explorer_frame.bind("<MouseWheel>", self._mousewheel)

        self._fill_explorer()

    def _configure_frame(self, event):
        """ Handles the event when self.explorer_frame is configured """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _mousewheel(self, event):
        """ Handles the mousewheel event on the explorer_frame """
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _reset_scrolling(self):
        """ Resets the scrolling of the explorer_frame to the beginning """
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0)

    def _move_back(self):
        """ Moves to the parent directory """
        self.change_path = False
        self.selected_path.set(os.path.dirname(self.path_to_show.get()))
        self.change_path = True
        self.path_to_show.set(os.path.dirname(self.path_to_show.get()))
        self._empty_explorer()
        self._fill_explorer()

    def _create_directory(self):
        """ Creates a new directory at the self.path_to_show location """
        while True:
            name = askstring("Creating directory", f"Enter the name of the directory to create\nThe directory will be created in: {self.path_to_show.get()}", allow_none=False)
            if name is None:
                break
            elif os.path.exists(join_paths(self.path_to_show.get(), name)):
                showwarning("Creating directory", "The given name already exists, please enter another one")
            else:
                os.mkdir(join_paths(self.path_to_show.get(), name))
                self.path_to_show.set(join_paths(self.path_to_show.get(), name))
                self.change_path = False
                self.selected_path.set(join_paths(self.path_to_show.get()))
                self.change_path = True
                self._empty_explorer()
                self._fill_explorer()
                break

    def _select(self, path: str):
        """ Changes the self.selected_path to the given path """
        self.change_path = False
        self.selected_path.set(path)
        self.change_path = True

    def _move_to(self, path: str):
        """ Changes the current directory to the given path """
        self.path_to_show.set(path)
        self.change_path = False
        self.selected_path.set(path)
        self.change_path = True
        self._empty_explorer()
        self._fill_explorer()

    def _empty_explorer(self):
        """ Empties the explorer_frame """
        for children in self.explorer_frame.winfo_children():
            children.destroy()

    def _fill_explorer(self):
        """ Fills the explorer_frame with the files at self.path_to_show """
        row = 0
        path = self.path_to_show.get()
        if os.path.isdir(path):
            for item in os.listdir(path):
                if os.path.isdir(join_paths(path, item)):  # directory
                    label = ctk.CTkLabel(self.explorer_frame, text=f"  {item}", compound="left", image=self.folder_image)
                    label.bind("<Button-1>", lambda event, p=join_paths(path, item): self._select(p))  # left click
                    label.bind("<Double-Button-1>", lambda event, p=join_paths(path, item): self._move_to(p))  # double left click
                    label.bind("<MouseWheel>", self._mousewheel)
                    label.grid(row=row, column=0, sticky="w", padx=3, pady=3)
                else:  # file
                    if not self.response_type == "directory":
                        if self.filetypes is None or self.filetypes is not None and f".{item.split(".")[-1]}" in self.filetypes:
                            label = ctk.CTkLabel(self.explorer_frame, text=f"  {item}", compound="left", image=self.file_image)
                            label.bind("<Button-1>", lambda event, p=join_paths(path, item): self._select(p))  # left click
                            label.bind("<MouseWheel>", self._mousewheel)
                            label.grid(row=row, column=0, sticky="w", padx=3, pady=3)
                row += 1
            self._reset_scrolling()

    def _user_path_changed(self, *args):
        """ Handles the event when self.selected_path is modified """
        if self.change_path:
            if os.path.isdir(self.selected_path.get()) and self.selected_path.get() != self.path_to_show.get():
                if not self.selected_path.get().endswith(" "):
                    self.path_to_show.set(self.selected_path.get())
                    self._empty_explorer()
                    self._fill_explorer()
            elif os.path.isfile(self.selected_path.get()) and os.path.dirname(self.selected_path.get()) != self.path_to_show.get():  # path to show changed
                if not os.path.dirname(self.selected_path.get()).endswith(" "):
                    self.path_to_show.set(os.path.dirname(self.selected_path.get()))
                    self._empty_explorer()
                    self._fill_explorer()

    def get_path(self):
        """Returns the selected path

        :return: selected path, "" if no paths were selected
        """
        if self.response_type == "file" and os.path.isfile(self.selected_path.get()):
            return self.selected_path.get()
        elif self.response_type == "directory" and os.path.isdir(self.selected_path.get()):
            return self.selected_path.get()
        else:
            return ""

    def move_to(self, path: str):
        """Changes the current directory to the given one

        :param path: path of the directory to move to
        """
        if os.path.isdir(path):
            self._move_to(path)
        else:
            raise ValueError(f"The given path isn't a directory: {path}")


class Filedialog(ctk.CTkToplevel):
    def __init__(self, responsetype: Literal["file", "directory"], title: str, filetypes: list[str] = None,
                 initialdir: str = None, initialfile: str = None, geometry: str = "400x550"):
        """Creates a filedialog instance to ask for a file / directory

        :param responsetype: type of the selected response: "file" / "directory"
        :param title: title of the widget
        :param filetypes: extension of the file to enter: ("text", ".txt"), None if the response should be a directory
        :param initialdir: initial directory to start the search from, None if initialfile is not None
        :param initialfile: initial file selected
        :param geometry: initial geometry of the toplevel, default is "400x500"
        """
        self.path = None

        super().__init__()
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.grab_set()  # make other windows not clickable

        self.title(title)
        self.geometry(geometry)

        self.protocol("WM_DELETE_WINDOW", self._kill_event)

        self.explorer = FileExplorer(self, responsetype, filetypes, initialdir, initialfile)
        self.ok_button = ctk.CTkButton(self, text="Ok", command=self._ok_event)
        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self._cancel_event)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.explorer.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.ok_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.cancel_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.bind("<Return>", self._ok_event)
        self.bind("<Escape>", self._cancel_event)

    def _ok_event(self, event=None):
        path = self.explorer.get_path()
        if path != "":
            self.path = path
            self.grab_release()
            self.destroy()
        else:
            showwarning("Entering path", "Please select a path")

    def _cancel_event(self, event=None):
        self.path = None
        self.grab_release()
        self.destroy()

    def _kill_event(self, event=None):
        self.path = None
        self.grab_release()
        self.destroy()

    def get_response(self) -> str | None:
        """ Waits until the dialog is closed and returns the path the user selected or None if the user cancelled """
        self.master.wait_window(self)
        return self.path


def askfile(title: str, filetypes: list[str] = None, initialdir: str = None, initialfile: str = None):
    """Asks for a file to select

    :param title: title of the widget
    :param filetypes: extension of the file to enter: ("text", ".txt"), None if the response should be a directory
    :param initialdir: initial directory to start the search from, None if initialfile is not None
    :param initialfile: initial file selected
    :return: path of the selected file, None if the user cancelled
    """
    dialog = Filedialog("file", title, filetypes, initialdir, initialfile)
    return dialog.get_response()


def askdir(title: str, initialdir: str = None):
    """Asks for a directory / folder to select

    :param title: title of the widget
    :param initialdir: initial directory to start the search from
    :return: path of the selected file, None if the user cancelled
    """
    dialog = Filedialog("directory", title, initialdir=initialdir)
    return dialog.get_response()
