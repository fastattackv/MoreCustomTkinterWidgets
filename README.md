# MoreCustomTkinterWidgets
By Fastattack, 2024

## Introduction
This module contains more, easy to use, customtkinter widgets
This file will present you the principal ones

## Modules

### SmoothFrame
This widget is a normal frame but with one upgrade: animations !

If you want to move the frame from one grid cell to another or one placing coordinates to another, you can use smooth_grid or smooth_place to move the frame to the given spot in a given time.

Inside the frame, you can still put other widgets

### FileExplorer
This class is used to navigate and select files directly in the interface (not a TopLevel).

It also comes with a class to ask for a file in a TopLevel (FileDialog).

The FileDialog class comes with prebuilt functions to ask for files more easily: askdir, askfile

### Selector
This class is used to select values in a list.

You give a list of values to the widget, and it creates a scrollable frame containing multiple checkboxes. When you want to retrieve the entries, you just call the get_selections method.

### Askdialog and Askvalue
Those two classes are TopLevels used to ask values (string / integer / float / boolean) to the user.

They come with functions to use them more easily: askstring, askinteger, askfloat, askyesno

### Message
This class is used to display messages (TopLevel) to inform the user about errors / what is happening in the app.

It comes with prebuilt functions to use it more easily: showinfo, showwarning, showerror

These functions existed in normal tkinter but didn't go in customtkinter.
