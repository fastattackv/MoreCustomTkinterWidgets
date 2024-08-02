# Patch notes for MoreCustomTkinterWidgets


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
- Selector: args and kwargs can now be passed to the super CTkFrame class


## v1.0.0
16/03/2024

Initial creation, contains `AskDialog`, `AskValue`, `FileExplorer`, `Message`, `Selector`, `SmoothFrame`
