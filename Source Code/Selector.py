import customtkinter as ctk
from customtkinter import ThemeManager


class Selector(ctk.CTkFrame):
    def __init__(self, master, names_list: list[str], multiple_choices=True, *args, **kwargs):
        """Selector widgets to select options in a list of options. Includes a search bar to find different elements faster.

        :param master: master window for the widget
        :param names_list: list of the possible options, they should all be different
        :param multiple_choices: Optional: if set to False, the user will be allowed to select only one item (default=True)
        :param args: args for the CTkFrame widget
        :param kwargs: kwargs for the CTkFrame widget
        """
        super().__init__(master, *args, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.search_var = ctk.StringVar(self)
        self.search_var.trace_add("write", self._search_modified)
        self.search_bar = ctk.CTkEntry(self, textvariable=self.search_var)
        self.empty_search_button = ctk.CTkButton(self, width=10, height=10, fg_color="transparent", border_color=ThemeManager.theme["CTkEntry"]["border_color"], border_width=2, text="X", command=self._empty_search)
        color = kwargs.pop("fg_color") if "fg_color" in kwargs else "transparent"
        self.checkboxes_frame = ctk.CTkScrollableFrame(self, fg_color=color, *args, **kwargs)
        self.search_bar.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")
        self.empty_search_button.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")
        self.checkboxes_frame.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky="nsew")

        self.checkboxes = []
        self.selected_indexes = []
        self.multiple_choices = multiple_choices

        if len(set(names_list)) == len(names_list):  # not 2 times the same item
            for index in range(len(names_list)):
                self.checkboxes.append(ctk.CTkCheckBox(self.checkboxes_frame, text=names_list[index], command=lambda a=index: self._selection(a)))
            self._search_modified()
        else:
            raise ValueError("There is two times or more the same item in the given names_list")

    def _selection(self, index: int):
        """ Internal method: selects / unselects the given index """
        if index in self.selected_indexes:
            self.selected_indexes.remove(index)
        else:
            if self.multiple_choices:
                self.selected_indexes.append(index)
            else:
                if self.selected_indexes:  # list not empty
                    for i in self.selected_indexes:
                        self.checkboxes[i].deselect()
                    self.selected_indexes.clear()
                    self.selected_indexes.append(index)
                else:
                    self.selected_indexes.append(index)

    def _reset_scroll(self):
        """ Internal method: scrolls back to the starting position """
        self.checkboxes_frame._parent_canvas.yview_moveto(0)

    def _search_modified(self, *args):
        """ Internal method: modifies the search """
        value = self.search_var.get()
        row = 0
        for x in range(len(self.checkboxes)):
            if self.checkboxes[x].cget("text").startswith(value):
                self.checkboxes[x].grid(row=row, column=0, pady=3, sticky="w")
                row += 1
            else:
                self.checkboxes[x].grid_forget()
        self._reset_scroll()

    def _empty_search(self):
        """ Internal method: empties the search bar """
        self.search_var.set("")

    def get_all_items(self) -> list:
        """ Returns all the items in the selector """
        return [checkbox.cget("text") for checkbox in self.checkboxes]

    def configure(self, require_redraw=False, **kwargs):
        if "names_list" in kwargs:
            names_list = kwargs.pop("names_list")
            if len(set(names_list)) == len(names_list):  # not 2 times the same item
                # destroy old widgets
                for checkbox in self.checkboxes:
                    checkbox.destroy()
                self.checkboxes.clear()
                self.selected_indexes.clear()
                # create new ones
                for index in range(len(names_list)):
                    self.checkboxes.append(ctk.CTkCheckBox(self.checkboxes_frame, text=names_list[index], command=lambda a=index: self._selection(a)))
                self._search_modified()
            else:
                raise ValueError("There is two times or more the same item in the given names_list")

        if "multiple_choices" in kwargs:
            multiple_choices = kwargs.pop("multiple_choices")
            self.multiple_choices = multiple_choices

        super().configure(require_redraw=require_redraw, **kwargs)

    def clear_selections(self):
        """ Clears the selections """
        for index in self.selected_indexes:
            self.checkboxes[index].deselect()
        self.selected_indexes.clear()

    def get_selections(self) -> list:
        """Returns the selected items

        :return: selected items, empty list if none were selected
        """
        return [self.checkboxes[index].cget("text") for index in self.selected_indexes]
