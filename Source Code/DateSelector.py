"""
This file contains the Calendar and DateSelector widgets
"""

import customtkinter as ctk
import tkinter as tk
import datetime
import os
from PIL import Image
from typing import Literal, Optional, Union, Tuple, Callable


def week_days_list_when_week_starts_with(weekday: Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"]) -> list[str]:
    """ Returns the list of the days of the week starting with the given day """
    full_days_list = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    if weekday in full_days_list:
        return_list = [weekday]
        split_index = full_days_list.index(weekday)
        return_list.extend(full_days_list[split_index + 1:])
        return_list.extend(full_days_list[:split_index])
        return return_list
    else:
        raise ValueError(f"The given weekday is not valid: {weekday}")


class Date:
    def __init__(self, day: int, month: int, year: int, hour: int = None, minute: int = None, date_format: Literal["dmy", "mdy", "ymd"] = "dmy"):
        """Class to verify if a date is correct and store it (minute, hour, day, month, year)

        :param day: day of the event (takes into account the rules for the leap years)
        :param month: month of the event
        :param year: year of the event
        :param hour: optional: hour of the event
        :param minute: optional: minute of the event (an hour must be entered to use the minute parameter)
        :param date_format: format of the date ("dmy", "mdy" or "ymd")
        """
        if type(year) is int:
            self.year = year
        else:
            raise TypeError(f"The value entered for the year is not an int: {type(year)}")

        if type(month) is int:
            if 1 <= month <= 12:
                self.month = month
            else:
                raise ValueError(f"The value given for the month is invalid: {month}")
        else:
            raise TypeError(f"The value entered for the month is not an int: {type(month)}")

        if type(day) is int:
            leap_year = True if year % 400 == 0 else False if year % 100 == 0 else True if year % 4 == 0 else False
            if (month in (1, 3, 5, 7, 8, 10, 12) and 1 <= day <= 31) or (month in (4, 6, 9, 11) and 1 <= day <= 30) or (month == 2 and not leap_year and 1 <= day <= 28) or (month == 2 and leap_year and 1 <= day <= 29):
                self.day = day
            else:
                raise ValueError(f"The value given for the day is invalid: {day} for the month {month} and year {year}")
        else:
            raise TypeError(f"The value entered for the day is not an int: {type(day)}")

        if hour is not None:
            if type(hour) is int:
                if 0 <= hour <= 23:
                    self.hour = hour
                else:
                    raise ValueError(f"The value given for the hour is invalid: {hour}")
            else:
                raise TypeError(f"The value entered for the hour is not an int: {type(hour)}")
        else:
            self.hour = None

        if minute is not None:
            if hour is not None:
                if type(minute) is int:
                    if 0 <= minute <= 59:
                        self.minute = minute
                    else:
                        raise ValueError(f"The value given for the minute is invalid: {minute}")
                else:
                    raise TypeError(f"The value entered for the minute is not an int: {type(minute)}")
            else:
                raise ValueError(f"Cannot enter a minute without an hour")
        else:
            self.minute = None

        if type(date_format) is str:
            if date_format in ["dmy", "mdy", "ymd"]:
                self.format = date_format
            else:
                raise ValueError(f"The given date_format is incorrect: {date_format}")
        else:
            raise TypeError(f"The value entered for the date_format is not a string: {type(date_format)}")

    def __str__(self):
        if self.format == "dmy":
            date = f"Date: {self.day}/{self.month}/{self.year}"  # "Date: d/m/y, h:m"
        elif self.format == "mdy":
            date = f"Date: {self.month}/{self.day}/{self.year}"  # "Date: m/d/y, h:m"
        else:
            date = f"Date: {self.year}/{self.month}/{self.day}"  # "Date: y/m/d, h:m"

        if self.hour is not None and self.minute is not None:
            return f"{date}, {self.hour}:{self.minute}"
        elif self.hour is not None:
            return f"{date}, {self.hour}h"
        else:
            return date

    def __eq__(self, other):
        if isinstance(other, Date):
            if self.day == other.day and self.month == other.month and self.year == other.year:
                if self.hour is not None and other.hour is not None:
                    if self.hour == other.hour:
                        if self.minute is not None and other.minute is not None:
                            if self.minute == other.minute:
                                return True
                            else:
                                return False
                        else:
                            return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        else:
            raise TypeError(f"Cannot compare {type(self)} and {type(other)}")

    def __lt__(self, other):
        if isinstance(other, Date):
            if self.year < other.year:
                return True
            elif self.year == other.year:
                if self.month < other.month:
                    return True
                elif self.month == other.month:
                    if self.day < other.day:
                        return True
                    elif self.day == other.day:
                        if self.hour is not None and other.hour is not None:
                            if self.hour < other.hour:
                                return True
                            elif self.hour == other.hour:
                                if self.minute is not None and other.minute is not None:
                                    if self.minute < other.minute:
                                        return True
            return False
        else:
            raise TypeError(f"Cannot compare {type(self)} and {type(other)}")

    def __le__(self, other):
        if isinstance(other, Date):
            if self.year <= other.year:
                return True
            elif self.year == other.year:
                if self.month <= other.month:
                    return True
                elif self.month == other.month:
                    if self.day <= other.day:
                        return True
                    elif self.day == other.day:
                        if self.hour is not None and other.hour is not None:
                            if self.hour <= other.hour:
                                return True
                            elif self.hour == other.hour:
                                if self.minute is not None and other.minute is not None:
                                    if self.minute <= other.minute:
                                        return True
            return False
        else:
            raise TypeError(f"Cannot compare {type(self)} and {type(other)}")

    def weekday(self) -> str:
        """ Returns the day of the week the date is ("mon", "tue", "wed", "thu", "fri", "sat" or "sun") """
        int_to_str_day_of_the_week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        return int_to_str_day_of_the_week[datetime.date(self.year, self.month, self.day).weekday()]

    def length_of_current_month(self) -> int:
        """ Returns the number of days in the current month """
        if self.month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif self.month in (4, 6, 9, 11):
            return 30
        else:  # february
            if True if self.year % 400 == 0 else False if self.year % 100 == 0 else True if self.year % 4 == 0 else False:  # leap year
                return 29
            else:
                return 28


class DateSelector(ctk.CTkFrame):
    def __init__(self,
                 master: any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 overwrite_preferred_drawing_method: Union[str, None] = None,

                 week_starts_with: Literal["mon", "tue", "wed", "thu", "fri", "sat", "sun"] = "mon",
                 default_date: Date = None,
                 callback: Callable[[], None] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 **kwargs):
        """DateSelector widget to select a date. Uses the same arguments as CTkFrame

        :param week_starts_with: day the week starts with, can be: "mon", "tue", "wed", "thu", "fri", "sat" or "sun"
        :param default_date: date selected by default, if None is given, the default date is today
        :param callback: function to call when a new date is selected
        """
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self._button_hover_color = ctk.ThemeManager.theme["CTkButton"]["hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)

        if type(week_starts_with) is str:
            if week_starts_with in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
                self.week_starts_with = week_starts_with
            else:
                raise ValueError(f"The given week_starts_with argument is invalid: {week_starts_with}")
        else:
            raise TypeError(f"The given week_starts_with argument is not a string: {type(week_starts_with)}")

        self.months_list = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

        if isinstance(default_date, Date):
            self.date = default_date
        elif default_date is None:
            date = datetime.datetime.now()
            self.date = Date(date.day, date.month, date.year)
        else:
            raise TypeError(f"The given default_date argument is not a Date instance: {type(default_date)}")

        if callable(callback) or callback is None:
            self._callback = callback
        else:
            raise ValueError(f"The given callback is not callable: {callback}")

        self.back_arrow_image = ctk.CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "Images/back_arrow_light.png")), Image.open(os.path.join(os.path.dirname(__file__), "Images/back_arrow_dark.png")))
        self.forward_arrow_image = ctk.CTkImage(Image.open(os.path.join(os.path.dirname(__file__), "Images/forward_arrow_light.png")), Image.open(os.path.join(os.path.dirname(__file__), "Images/forward_arrow_dark.png")))

        self.top_frame = ctk.CTkFrame(self, fg_color=self._fg_color)
        self.back_button = ctk.CTkButton(self.top_frame, text="", image=self.back_arrow_image, command=self._back, fg_color=self._fg_color, border_color=self._border_color, border_width=2, width=30)
        self.forward_button = ctk.CTkButton(self.top_frame, text="", image=self.forward_arrow_image, command=self._forward, fg_color=self._fg_color, border_color=self._border_color, border_width=2, width=30)
        self.year_var = ctk.IntVar(self.top_frame, self.date.year)
        self.year_var.trace_add("write", self._year_changed)
        self.year_entry = ctk.CTkEntry(self.top_frame, textvariable=self.year_var, width=100, justify="center")
        self.month_label = ctk.CTkLabel(self.top_frame, text=self.months_list[self.date.month - 1])
        self.back_button.grid(row=0, column=0, padx=2, pady=2)
        self.year_entry.grid(row=0, column=1, padx=2, pady=2)
        self.forward_button.grid(row=0, column=2, padx=2, pady=2)
        self.month_label.grid(row=1, column=0, columnspan=3, padx=2, pady=2)

        self.days_frame = ctk.CTkFrame(self, fg_color=self._fg_color)
        self.week_days_labels_dict = {day: ctk.CTkLabel(self.days_frame, text=day) for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]}
        self.regrid_weekdays()
        self.days_buttons_list = [ctk.CTkButton(self.days_frame, text=str(day), fg_color=self._fg_color, hover_color=self._button_hover_color, width=25, command=lambda x=day: self._selected_day(x)) for day in range(1, 32)]
        self.previous_selected_day_index = self.date.day - 1

        self.top_frame.grid(row=0, column=0, padx=1, pady=1)
        self.days_frame.grid(row=1, column=0, padx=1, pady=1)
        self._actualize_days()

    def configure(self, require_redraw=False, **kwargs):
        if "fg_color" in kwargs:
            fg_color = kwargs["fg_color"]
            self.top_frame.configure(fg_color=fg_color)
            self.back_button.configure(fg_color=fg_color)
            self.forward_button.configure(fg_color=fg_color)
            self.days_frame.configure(fg_color=fg_color)
            for index in range(len(self.days_buttons_list)):
                self.days_buttons_list[index].configure(fg_color=fg_color)

        if "button_hover_color" in kwargs:
            button_hover_color = kwargs.pop("button_hover_color")
            self._button_hover_color = ctk.ThemeManager.theme["CTkButton"]["hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
            self.days_buttons_list[self.previous_selected_day_index].configure(fg_color=self._button_hover_color)

        if "week_starts_with" in kwargs:
            week_starts_with = kwargs.pop("week_starts_with")
            if type(week_starts_with) is str:
                if week_starts_with in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
                    self.week_starts_with = week_starts_with
                    self.regrid_weekdays()
                    self._actualize_days()
                else:
                    raise ValueError(f"The given week_starts_with argument is invalid: {week_starts_with}")
            else:
                raise TypeError(f"The given week_starts_with argument is not a string: {type(week_starts_with)}")

        if "callback" in kwargs:
            callback = kwargs.pop("callback")
            if callable(callback) or callback is None:
                self._callback = callback
            else:
                raise ValueError(f"The given callback is not callable: {callback}")

        super().configure(require_redraw=require_redraw, **kwargs)

    def _check_if_day_is_correct(self):
        """ Changes the day if it not possible (ex: june 31st is retransformed in june 30th) """
        if self.date.day > self.date.length_of_current_month():
            self.date.day = self.date.length_of_current_month()

    def _back(self):
        """ Called when the back button is pressed """
        if self.date.month == 1:
            self.date.month = 12
            self.date.year -= 1
            self.year_var.set(self.date.year)
        else:
            self.date.month -= 1
        self.month_label.configure(text=self.months_list[self.date.month - 1])
        self._check_if_day_is_correct()
        self._actualize_days()

    def _forward(self):
        """ Called when the forward button is pressed """
        if self.date.month == 12:
            self.date.month = 1
            self.date.year += 1
            self.year_var.set(self.date.year)
        else:
            self.date.month += 1
        self.month_label.configure(text=self.months_list[self.date.month - 1])
        self._check_if_day_is_correct()
        self._actualize_days()

    def _year_changed(self, *args):
        """ Called when the year is changed """
        self._check_if_day_is_correct()
        self._actualize_days()

    def _selected_day(self, day: int):
        """ Called when a day button is pressed """
        self.date.day = day
        self._actualize_days()

    def _actualize_days(self):
        """ Actualizes the days buttons """
        temp_date = Date(1, self.date.month, self.date.year)
        row = 1
        column = week_days_list_when_week_starts_with(self.week_starts_with).index(temp_date.weekday())
        for day in range(self.date.length_of_current_month()):
            self.days_buttons_list[day].grid(row=row, column=column)
            column += 1
            if column > 6:
                column = 0
                row += 1
        for day in range(self.date.length_of_current_month(), 31):
            self.days_buttons_list[day].grid_forget()
        self.days_buttons_list[self.previous_selected_day_index].configure(fg_color=self._fg_color)
        self.days_buttons_list[self.date.day - 1].configure(fg_color=self._button_hover_color)
        self.previous_selected_day_index = self.date.day - 1
        if self._callback is not None:
            self._callback()

    def regrid_weekdays(self):
        days_list = week_days_list_when_week_starts_with(self.week_starts_with)
        column = 0
        for day in days_list:
            self.week_days_labels_dict[day].grid(row=0, column=column)
            column += 1

    def get(self) -> Date:
        """ Returns the current selected date """
        return self.date


class DateSelectorButton(ctk.CTkButton):
    def __init__(self,
                 master: any,

                 callback: Union[Callable[[], None], None] = None,  # called when the selected date is changed
                 restrained_to_master: bool = False,
                 default_date: Date | None = None,

                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,
                 border_spacing: int = 2,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 round_width_to_even_numbers: bool = True,
                 round_height_to_even_numbers: bool = True,

                 text: str = "MCTkDatePicker",
                 font: Optional[Union[tuple, ctk.CTkFont]] = None,
                 textvariable: Union[tk.Variable, None] = None,
                 image: Union[ctk.CTkImage, None] = None,
                 state: str = "normal",
                 hover: bool = True,
                 compound: str = "left",
                 anchor: str = "center",
                 **kwargs):
        """DatePicker widget to select a date. All arguments for ctk.CTkButton are valid except "command"

        :param callback: function to call when a new date is selected
        :param restrained_to_master: if set to True, the popup frame will not be able to get out of the direct master of the widget, otherwise the popup menu will be able to expand in the whole window
        :param default_date: date selected by default
        """
        super().__init__(master, width, height, corner_radius, border_width, border_spacing,
                         bg_color, fg_color, hover_color, border_color, text_color, text_color_disabled,
                         background_corner_colors, round_width_to_even_numbers, round_height_to_even_numbers,
                         text, font, textvariable, image, state, hover, self._on_clicked, compound, anchor, **kwargs)
        if callback is not None:
            if callable(callback):
                self._callback = callback
            else:
                raise TypeError(f"The given callback is not callable: {callback}")

        if type(restrained_to_master) is bool:
            self._restrained_to_master = restrained_to_master
        else:
            raise TypeError(f"The given restrained_to_master argument is not a boolean: {type(restrained_to_master)}")

        if isinstance(default_date, Date):
            self._date = default_date
        elif default_date is None:
            date = datetime.datetime.now()
            self._date = Date(date.day, date.month, date.year)
        else:
            raise TypeError(f"The given default_date argument is not a Date instance: {type(default_date)}")

        if restrained_to_master:
            self._popup_frame = ctk.CTkFrame(master)
        else:
            while not isinstance(master, (tk.Tk, ctk.CTk, tk.Toplevel, ctk.CTkToplevel)):
                master_name = master.winfo_parent()
                master = master._nametowidget(master_name)
            self._popup_frame = DateSelector(master)

    def _on_clicked(self):
        """ Called when the button is clicked """
        if self._popup_frame.place_info():  # is currently shown
            self._popup_frame.place_forget()
        else:  # is not currently shown
            x = self.winfo_x() + self.winfo_width()
            y = self.winfo_y() + self.winfo_height()
            self._popup_frame.place(x=x, y=y)
            self._popup_frame.update()
            width = self._popup_frame.winfo_width()
            height = self._popup_frame.winfo_height()
            master_width = self._popup_frame.master.winfo_width()
            master_height = self._popup_frame.master.winfo_height()

            if x + width > master_width or y + height > master_height:  # does not fit: search where can it fit
                if x + width > master_width:  # does not fit to the right of the button
                    new_x = master_width - width
                else:  # fits to the right of the button
                    new_x = x
                if y + height > master_height:  # cannot fit under the button
                    if height > self.winfo_y():  # cannot fit above the button
                        new_y = y
                    else:  # can fit above the button
                        new_y = self.winfo_y() - height
                else:  # can fit under the button
                    new_y = y
                self._popup_frame.place(x=new_x, y=new_y)

    def get(self) -> Date:
        return self._date



win = ctk.CTk()
win.title("MoreCustomTkinterWidgets examples !")
win.geometry("500x500")

date_selector = DateSelector(win, default_date=Date(1, 1, 2000, date_format="dmy"))
date_selector.pack()

win.mainloop()