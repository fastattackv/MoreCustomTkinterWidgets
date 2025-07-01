# Patch notes for MoreCustomTkinterWidgets


## v5.0.0
01/07/2025

Novelties:
- New widgets: `DateSelector` and `DateSelectorButton`
  - Used to ask the user to select a date with an easy interface


## v4.1.2
26/03/2025

Corrections:
- Selector
  - Corrected the `Selector.get_selections()` method (it returned widgets instead of their names)

## v4.1.1
26/03/2025

Corrections:
- Selector
  - could not configure the items in the selector using the `Selector.configure_selector()` method.


## v4.1.0
21/12/2024

Novelties:
- Selector:
  - New functionnality: the search bar. Allows to easily narrow the search of an item.


## v4.0.1
26/08/2024

Corrections:
- `Separator`: removed the test code (prevented the entire module from being used)


## v4.0.0
26/08/2024

Novelties:
- New widget: `Separator`
  - Used just like the separator in classic tkinter, this widget allows to separate other widgets more clearly (draws a line to separate widgets).
  - For now the separator cannot expand by itself using `Separator.pack(expand=True, fill="both")` or `Separator.grid(sticky="nswe")`, you have to enter the size of the separator manually.


## v3.0.1
23/08/2024

Corrections:
- `AnimatedImage`: removed the test code (prevented the entire module from being used)


## v3.0.0
02/08/2024

Novelties:
- New utility class: `AnimatedImage`
  - Used like `CTkImage` but allows to run an animation if an image sequence (FLI/FLC, GIF) was given.
  - You can start the animation, and it will run until you call the method to stop it or you can run it for a given time.


## v2.0.0
29/03/2024

Novelties:
- New utility class: `BetterCTkImage`
  - Used like `CTkImage` but allows for rounded corners for the image (and you can directly pass the image path instead of an Image instance when creating the class)
  - You can configure the radius of corner rounding by using `BetterCTkImage.configure()` and the image will update automatically everywhere it is used.


## v1.1.0
17/03/2024

Novelties:
- Selector:
  - new parameter: `multiple_choices`: if set to False, only one item can be selected
  - new method: `get_all_items()`: returns all the items in the selector
  - new method: `configure_selector()`: allows to change the items in the selector or the multiple_choices parameter
  - new method: `clear_selections()`: clears the items selections
- FileExplorer:
  - new method: `move_to()`: changes the current directory of the explorer to the given one


## v1.0.1
16/03/2024

Corrections:
- `Selector`: args and kwargs can now be passed to the super CTkFrame class


## v1.0.0
16/03/2024

Initial creation, contains `AskDialog`, `AskValue`, `FileExplorer`, `Message`, `Selector`, `SmoothFrame`
