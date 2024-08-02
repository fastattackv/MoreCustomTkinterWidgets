# MoreCustomTkinterWidgets
By Fastattack, 2024

[![Pypi](https://img.shields.io/pypi/v/MoreCustomTkinterWidgets?label=Pypi)](https://pypi.org/project/MoreCustomTkinterWidgets)
[![GitHub - Total commits](https://img.shields.io/github/commit-activity/t/fastattackv/MoreCustomTkinterWidgets?label=Total%20GitHub%20commits&color=darkblue)](https://github.com/fastattackv/MoreCustomTkinterWidgets)
[![GitHub - Last commit](https://img.shields.io/github/last-commit/fastattackv/MoreCustomTkinterWidgets?label=Last%20GitHub%20commit&color=darkblue)](https://github.com/fastattackv/MoreCustomTkinterWidgets)
[![Pypi - Monthly downloads](https://img.shields.io/pypi/dm/MoreCustomTkinterWidgets)](https://pypi.org/project/MoreCustomTkinterWidgets)
[![Pypi - Total downloads](https://static.pepy.tech/personalized-badge/MoreCustomTkinterWidgets?period=total&units=international_system&left_color=grey&right_color=green&left_text=Total%20Downloads)](https://pypi.org/project/MoreCustomTkinterWidgets)
[![Lines number](https://tokei.rs/b1/github/fastattackv/MoreCustomTkinterWidgets?category=lines)](https://github.com/fastattackv/MoreCustomTkinterWidgets/tree/main/Source%20Code)

> [!NOTE]
> The package is cross-platform, but the Message class will only be able to create sounds if the winsound module is installed (only available on windows)

## Introduction
This module contains more, easy to use, customtkinter widgets.

This file will present you the best ones.

See [^1] for the mentions.

## How to install
To install the package, you should use pip. Install the package with the following command: `pip install MoreCustomTkinterWidgets`

## Widgets

[![Examples](https://img.shields.io/badge/Examples_for_all_widgets-red)](Examples.md)
[![Patch Notes](https://img.shields.io/badge/Patch_Notes-yellow)](Patch%20notes.md)

### SmoothFrame
This widget is a normal frame but with one upgrade: animations !

If you want to move the frame from one grid cell to another or one placing coordinates to another, you can use smooth_grid or smooth_place to move the frame to the given spot in a given time.

Inside the frame, you can still put other widgets

### FileExplorer
This class is used to navigate and select files directly in the interface (not a TopLevel).

It also comes with a class to ask for a file in a TopLevel (FileDialog).

The FileDialog class comes with prebuilt functions to ask for files more easily: askdir, askfile

### AnimatedImage
This class is used like `CTkImage` but allows to run an animation if an image sequence (FLI/FLC, GIF) was given.

You can start the animation, and it will run until you call the method to stop it, or you can run it for a given time.

### BetterCTkImage
This class is used like CTkImage, but you can round the images corners !

You can configure the radius of corner rounding by using `BetterCTkImage.configure()` and the image will update automatically everywhere it is used.

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


[^1]: Mentions:

    Used modules: customtkinter, Pillow
    
    Used services for README statistics: [shields.io](https://img.shields.io), [tokei.rs](https://github.com/XAMPPRocky/tokei), [pepy.tech](https://github.com/psincraian/pepy)
