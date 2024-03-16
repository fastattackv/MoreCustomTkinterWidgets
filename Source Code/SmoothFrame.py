import customtkinter as ctk
from typing import Optional, Union, Tuple
import threading
import time


_x, _y = 0, 0  # variables for the get_coordinates_from_grid function


def _get_coordinates_of_frame(frame):
    """ Internal function, assigns the coordinates of the given frame to _x and _y """
    global _x, _y
    _x = frame.winfo_x()
    _y = frame.winfo_y()
    frame.destroy()


def get_coordinates_from_grid(master, column: int, row: int, padx=0, pady=0, ipadx=0, ipady=0) -> tuple[int, int]:
    """Returns the coordinates of the given grid cell

    :param master: master to search the coordinates in
    :param column: column of the cell to obtain the coordinates from
    :param row: row of the cell to obtain the coordinates from
    :param padx: padding in x direction
    :param pady: padding in y direction
    :param ipadx: internal padding in x direction
    :param ipady: internal padding in y direction
    :return: tuple containing the x and y coordinates of the given grid cell
    """
    temp_frame = ctk.CTkFrame(master, fg_color="transparent", height=1, width=1)
    temp_frame.grid(row=row, column=column, sticky="nw", padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
    temp_frame.after(20, lambda: _get_coordinates_of_frame(temp_frame))
    temp_frame.wait_window()
    return _x, _y


class SmoothFrame(ctk.CTkFrame):
    """ Basic CTkFrame but with animations for moving the frame using grid and place """
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
                 **kwargs):
        # transfers frame arguments to CTkFrame class
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.time_between_each_cycle = 0
        self.remaining_cycles = 0
        self.current_coordinates = (0, 0)
        self.coordinates_modifiers = (0, 0)  # values to add to the coordinates of the frame on each cycle
        self.final_parameters = []

    def _smooth_place(self):
        """ Internal method, creates the movement animation """
        # animation
        while self.remaining_cycles > 0:
            self.current_coordinates = (self.current_coordinates[0] + self.coordinates_modifiers[0], self.current_coordinates[1] + self.coordinates_modifiers[1])
            self.place(x=self.current_coordinates[0], y=self.current_coordinates[1])
            self.remaining_cycles -= 1
            time.sleep(self.time_between_each_cycle)

        # final place
        self.place(
            x=self.final_parameters[0],
            y=self.final_parameters[1],
            relx=self.final_parameters[2],
            rely=self.final_parameters[3],
            anchor=self.final_parameters[4],
            relwidth=self.final_parameters[5],
            relheight=self.final_parameters[6],
            bordermode=self.final_parameters[7]
        )

        # resetting variables
        self.time_between_each_cycle = 0
        self.remaining_cycles = 0
        self.current_coordinates = (0, 0)
        self.coordinates_modifiers = (0, 0)
        self.final_parameters.clear()

    def smooth_place(self, time_to_move: float, x: int, y: int, relx=0, rely=0, anchor="nw", relwidth: int = "", relheight: int = "", bordermode="inside", frequency=120):
        """Moves the frame at the given coordinates in the given time

        :param time_to_move: duration of the animation in seconds (do not put less than 0.05 or the animation might go crazy)
        :param frequency: frequency of the places per second = "smoothness" of the animation (120Hz by default), should be set to the monitor's refresh rate if possible
        :param x: x coordinates to place the frame at
        :param y: y coordinates to place the frame at
        :param relx: locate anchor of this widget between 0.0 and 1.0 relative to width of master (1.0 is right edge)
        :param rely: locate anchor of this widget between 0.0 and 1.0 relative to height of master (1.0 is bottom edge)
        :param anchor: "nsew" (or subset) - position anchor according to given direction
        :param relwidth: width of this widget between 0.0 and 1.0 relative to width of master (1.0 is the same width as the master)
        :param relheight: height of this widget between 0.0 and 1.0 relative to height of master (1.0 is the same height as the master)
        :param bordermode: "inside" or "outside" - whether to take border width of master widget into account
        """
        place_infos = self.place_info()
        if place_infos:  # has been placed
            self.time_between_each_cycle = 1 / frequency - 0.000337  # the 0.000337 is the approximate time each placement takes, it is substracted to the time between each cycle so the global time is closer to the time_to_move
            self.remaining_cycles = time_to_move * frequency
            self.current_coordinates = (int(place_infos["x"]), int(place_infos["y"]))
            self.coordinates_modifiers = ((x - self.current_coordinates[0]) / self.remaining_cycles, (y - self.current_coordinates[1]) / self.remaining_cycles)
            self.final_parameters = [x, y, relx, rely, anchor, relwidth, relheight, bordermode]
            threading.Thread(target=self._smooth_place).start()
        else:  # has not already been placed
            self.place(
                x=x,
                y=y,
                relx=relx,
                rely=rely,
                anchor=anchor,
                relwidth=relwidth,
                relheight=relheight,
                bordermode=bordermode
            )

    def _smooth_grid(self):
        """ Internal method, creates the movement animation """
        # animation
        while self.remaining_cycles > 0:
            self.current_coordinates = (self.current_coordinates[0] + self.coordinates_modifiers[0], self.current_coordinates[1] + self.coordinates_modifiers[1])
            self.place(x=self.current_coordinates[0], y=self.current_coordinates[1])
            self.remaining_cycles -= 1
            time.sleep(self.time_between_each_cycle)
        self.place_forget()

        # final grid
        self.grid(
            column=self.final_parameters[0],
            row=self.final_parameters[1],
            columnspan=self.final_parameters[2],
            rowspan=self.final_parameters[3],
            sticky=self.final_parameters[4],
            padx=self.final_parameters[5],
            pady=self.final_parameters[6],
            ipadx=self.final_parameters[7],
            ipady=self.final_parameters[8]
        )

        # resetting variables
        self.time_between_each_cycle = 0
        self.remaining_cycles = 0
        self.current_coordinates = (0, 0)
        self.coordinates_modifiers = (0, 0)
        self.final_parameters.clear()

    def smooth_grid(self, time_to_move: float, column: int, row: int, columnspan=1, rowspan=1, sticky="", padx=0, pady=0, ipadx=0, ipady=0, frequency=120):
        """Moves the widget to the given coordinates with an animation

        :param time_to_move: time (in s) to move the widget to the new position
        :param frequency: frequency of the places per second = "smoothness" of the animation (120Hz by default), should be set to the monitor's refresh rate if possible
        :param column: column (x axis) to grid the frame to
        :param row: row (y axis) to grid the frame to
        :param columnspan: number of columns the frame will expand in (1 by default)
        :param rowspan: number of rows the frame will expand in (1 by default)
        :param sticky: which sides to expand to if cell is too large ("n", "s", "e" or "w" or multiple at once)
        :param padx: padding in x direction
        :param pady: padding in y direction
        :param ipadx: internal padding in x direction
        :param ipady: internal padding in y direction
        """
        if self.grid_info():  # has been gridded
            start_x = self.winfo_x()
            start_y = self.winfo_y()
            self.place(x=start_x, y=start_y)  # removes the widget from the grid so the end coordinates are correct
            x, y = get_coordinates_from_grid(self.master, column, row, padx, pady, ipadx, ipady)

            self.time_between_each_cycle = 1 / frequency - 0.00034  # the 0.00034 is the approximate time each placement takes, it is substracted to the time between each cycle so the global time is closer to the time_to_move
            self.remaining_cycles = time_to_move * frequency
            self.current_coordinates = (start_x, start_y)
            self.coordinates_modifiers = ((x - self.current_coordinates[0]) / self.remaining_cycles, (y - self.current_coordinates[1]) / self.remaining_cycles)
            self.final_parameters = [column, row, columnspan, rowspan, sticky, padx, pady, ipadx, ipady]
            threading.Thread(target=self._smooth_grid).start()
        else:  # has not already been gridded
            self.grid(
                column=column,
                row=row,
                columnspan=columnspan,
                rowspan=rowspan,
                sticky=sticky,
                padx=padx,
                pady=pady,
                ipadx=ipadx,
                ipady=ipady
            )
