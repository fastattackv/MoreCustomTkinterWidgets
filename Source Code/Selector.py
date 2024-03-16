import customtkinter as ctk


class Selector(ctk.CTkScrollableFrame):
    def __init__(self, master, items: list, *args, **kwargs):
        """Selector widgets to select options in a list of options

        :param master: master window for the widget
        :param items: list of the possible options, only different items
        :param args: args for the ScrollableFrame widget
        :param kwargs: kwargs for the ScrollableFrame widget
        """
        super().__init__(master, *args, **kwargs)

        added_items = []
        for x in range(len(items)):
            if str(items[x]) not in added_items:
                added_items.append(str(items[x]))
                ctk.CTkCheckBox(self, text=str(items[x])).grid(row=x, column=0, padx=3, pady=3, sticky="w")
            else:
                raise ValueError(f"There is two times or more the same value in the items: {str(items[x])}")

    def get_selections(self) -> list:
        """Returns the selected items

        :return: selected items, empty list if none were selected
        """
        selected_items = []
        for widget in self.winfo_children():
            if widget.get():
                selected_items.append(widget.cget("text"))
        return selected_items
