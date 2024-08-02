# Examples for MoreCustomTkinterWidgets

By Fastattack, for version 1.0

## Introduction

This file will teach and show you how to use the widgets in the MoreCustomTkinterWidgets module.

## Examples

### SmoothFrame

The `SmoothFrame` is used like a normal frame and is moved using the smooth_grid or smooth_place methods.
```python
import customtkinter as ctk
import MoreCustomTkinterWidgets as mctk

win = ctk.CTk()
win.title("MoreCustomTkinterWidgets examples !")
win.geometry("500x500")

frame = mctk.SmoothFrame(win, fg_color="red")
button = ctk.CTkButton(frame, text="Click me!", command=lambda: frame.smooth_place(1, 200, 200))
button.pack(padx=10, pady=10)
frame.place(x=0, y=0)

win.mainloop()
```
This code produces the following result (but at 120Hz of course ;) ):

![SmoothFrame example](Example%20files/SmoothFrame_example.gif)

---

### FileExplorer

The `FileExplorer` class is a widget used to select files or directories.
```python
import customtkinter as ctk
import MoreCustomTkinterWidgets as mctk

win = ctk.CTk()
win.title("MoreCustomTkinterWidgets examples !")
win.geometry("500x500")

file_explorer = mctk.FileExplorer(win, "file", width=300, height=400)
file_explorer.pack()

win.mainloop()
```
This code produces the following result:

![FileExplorer example](Example%20files/FileExplorer_example.png)

```python
import MoreCustomTkinterWidgets as mctk

selected_path = mctk.askfile("Title")
```
And this code produces the following result (in a TopLevel):

![FileDialog example](Example%20files/FileDialog_example.png)

---

### AnimatedImage

The `AnimatedImage` class allows to easily use animated images (like gifs).
```python
import customtkinter as ctk
import MoreCustomTkinterWidgets as mctk

win = ctk.CTk()
win.title("MoreCustomTkinterWidgets examples !")
win.geometry("400x300")

image = mctk.AnimatedImage("loading.gif", size=(100, 100))
label = ctk.CTkLabel(win, text="", image=image)
label.pack()

image.start_animation()

win.mainloop()
```
This code produces the following result:

![AnimatedImage example](Example%20files/AnimatedImage_example.gif)

---

### BetterCTkImage

The `BetterCTkImage` class allows to round the corners of a given image.
```python
import customtkinter as ctk
import MoreCustomTkinterWidgets as mctk

win = ctk.CTk()
win.title("MoreCustomTkinterWidgets examples !")
win.geometry("400x300")

image = mctk.BetterCTkImage(light_image="duck_image.png", size=(200, 200), rounded_corner_radius=50)
label = ctk.CTkLabel(win, text="", image=image)
label.pack()

win.mainloop()
```
This code produces the following result:

![BetterCTkImage example](Example%20files/BetterCTkImage_example.png)

---

### Selector

The `Selector` class allows to easily create a list of checkboxes to ask the user to select one or multiple choices. 
```python
import customtkinter as ctk
import MoreCustomTkinterWidgets as mctk

win = ctk.CTk()
win.title("MoreCustomTkinterWidgets examples !")
win.geometry("500x500")

selector = mctk.Selector(win, ["item1", "item2", "item3"])
selector.pack()

win.mainloop()
```
This code produces the following result:

![Selector example](Example%20files/Selector_example.png)

---

### AskDialog

The `AskDialog` class allows to ask yes / no to the user.
```python
import MoreCustomTkinterWidgets as mctk

response = mctk.askyesno("Title", "Message")
```
This code produces the following result:

![AskDialog example](Example%20files/AskDialog_example.png)

---

### AskValue

The `AskValue` class allows to ask a value to the user.
````python
import MoreCustomTkinterWidgets as mctk

response = mctk.askstring("Title", "Message")
````
This code produces the following result:

![AskValue example](Example%20files/AskValue_example.png)

---

### Message

The `Message` class allows to show messages (info / warning / error) to the user:
```python
import MoreCustomTkinterWidgets as mctk

mctk.showerror("Title", "Error message")
```
This code produces the following result:

![Message example](Example%20files/Message_example.png)
