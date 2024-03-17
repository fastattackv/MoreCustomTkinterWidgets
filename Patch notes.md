# Patch notes for MoreCustomTkinterWidgets


## v1.1.0
17/03/2024

Novelties:
- Selector:
  - new parameter: multiple_choices: if set to False, only one item can be selected
  - new method: get_all_items(): returns all the items in the selector
  - new method: configure_selector(): allows to change the items in the selector or the multiple_choices parameter
  - new method: clear_selections(): clears the items selections
- FileExplorer:
  - new method: move_to(): changes the current directory of the explorer to the given one


## v1.0.1
16/03/2024

Corrections:
- Selector: args and kwargs can now be passed to the super CTkFrame class


## v1.0.0
16/03/2024

Initial creation, contains AskDialog, AskValue, FileExplorer, Message, Selector, SmoothFrame
