# Imports
from tkinter import Toplevel, Label, Entry, Button
from .showcase_template import ShowcaseTemplate
import re

# Meta
MODULE_NAME = "Drawing a line with a linear function (y=mx+b)"
MODULE_AUTHOR = "R1DF"

# Function Inputter Toplevel
class FunctionInputter(Toplevel):
    def __init__(self, showcase, master_window):
        # Inheritance
        self.master_showcase = showcase
        self.master_window = master_window
        super().__init__(self.master_window)

        # Setup
        self.title("Linear Function Entry (Physics Showcase)")
        self.geometry("400x100")
        self.resizable(False, False)

        # Widgets
        self.insert_function_label = Label(self, text="Insert linear function: [example: \"y=3x-2\"]")
        self.insert_function_label.pack()

        self.linear_function_entry = Entry(self, width=13)
        self.linear_function_entry.pack()

        self.draw_button = Button(self, text="Draw", command=self.infer_inputted_function)
        self.draw_button.pack()

        self.details_label = Label(self, text="")
        self.details_label.pack()

        # Can't be closed (only closable by closing main window)
        self.protocol("WM_DELETE_WINDOW", lambda: None)

    def infer_inputted_function(self):
        linear_function_input = self.linear_function_entry.get().lower().strip().replace(" ", "")  # No spaces!

        # Viewing
        if linear_function_input.startswith("y=") and linear_function_input.count("x") == 1:
            split_determiner = 2

        elif linear_function_input.startswith("f(x)") and linear_function_input.count("x") == 2:
            split_determiner = 5

        else:
            self.details_label.config(text=f"Invalid input entered!", fg="RED")
            return

        linear_expression = linear_function_input[split_determiner:]
        match_query = re.search(r"^-?(\d+(\.\d+)?)?x([+-]\d+(\.\d+)?)?$", linear_expression)
        if not match_query:
            self.details_label.config(text=f"Invalid input entered!", fg="RED")
            return

        # Determining gradients
        function_halves = linear_expression.split("x")
        gradient = float(1 if not function_halves[0] else -1 if function_halves[0] == "-" else function_halves[0])
        y_intercept = float(function_halves[1] if function_halves[1] else 0)

        self.master_showcase.draw(gradient, y_intercept)
        self.details_label.config(text=f"Expression {linear_expression} drawn successfully!", fg="GREEN")
        return

#  Canvas class (must be named as Showcase)
class Showcase(ShowcaseTemplate):
    def __init__(self, master):
        # Inheritance
        super().__init__(master)

        # Showcase attributes
        self.function_line = None
        self.abscissa_line = self.create_line(
            0,
            self.master.HEIGHT // 2,
            self.master.WIDTH,
            self.master.HEIGHT // 2
        )
        self.ordinate_line = self.create_line(
            self.master.WIDTH // 2,
            0,
            self.master.WIDTH // 2,
            self.master.HEIGHT
        )

        # Offsets (not TICK offsets) determine how much does the distance between ticks on a plane mean in units of
        # length (e.g. 1 tick up is 2 units high and 1 tick to the right is 2 units to the right)
        self.unit_offset = 1

        # Ensuring drawing out ticks is possible
        self.has_ticks = (self.master.WIDTH % 20 == 0) and (self.master.HEIGHT % 20 == 0)  # TODO figure out limits for when poogram works
        if self.has_ticks:
            # Making calculations to draw "ticks" (small lines that space out coordinate points)
            tick_offset_1 = self.master.WIDTH // 20   # 20 is constant. Setting the value to anything else breaks everything
            tick_offset_2 = self.master.HEIGHT // 20
            self.tick_offset = min(tick_offset_1, tick_offset_2)
            self.x_ticks_amount = self.master.WIDTH // self.tick_offset
            self.y_ticks_amount = self.master.HEIGHT // self.tick_offset

            self.x_ticks = []
            self.y_ticks = []
            self.x_units = []
            self.y_units = []

            # Drawing out ticks from calculations
            for tick in range(1, self.x_ticks_amount + 1):
                self.x_ticks.append(self.create_line(
                    tick * self.tick_offset,
                    (self.master.HEIGHT // 2) - 5,
                    tick * self.tick_offset,
                    (self.master.HEIGHT // 2) + 5
                ))

            for tick in range(1, self.y_ticks_amount + 1):
                self.y_ticks.append(self.create_line(
                    (self.master.WIDTH // 2) - 5,
                    tick * self.tick_offset,
                    (self.master.WIDTH // 2) + 5,
                    tick * self.tick_offset
                ))

            # Drawing out units
            x_mid_tick_value = len(self.x_ticks) // 2
            for tick in self.x_ticks:
                unit_shown = self.unit_offset * ((self.x_ticks.index(tick) + 1) - x_mid_tick_value)
                if unit_shown == 0:
                    continue  # No need to draw out 0

                tick_coordinates = self.bbox(tick)
                self.x_units.append([self.create_text(
                    tick_coordinates[2] - 2,
                    (self.master.HEIGHT // 2) + 13,
                    text=f"{unit_shown}",
                    font="Arial 8"
                ), unit_shown])  # [unit object, unit shown]

            y_mid_tick_value = len(self.y_ticks) // 2
            for tick in self.y_ticks:
                unit_shown = self.unit_offset * (y_mid_tick_value - (self.y_ticks.index(tick) + 1))
                if unit_shown == 0:
                    continue  # No need to draw out 0

                tick_coordinates = self.bbox(tick)
                self.x_units.append([self.create_text(
                    (self.master.WIDTH // 2) + 13,
                    tick_coordinates[3] - 2,
                    text=f"{unit_shown}",
                    font="Arial 8"
                ), unit_shown])  # [unit object, unit shown]

        # Create toplevel
        self.function_inputter = FunctionInputter(self, self.master)

    def get_relative_coordinates(self, coordinates):
        # Calculating Cartesian coordinates with account to unit offset
        cartesian_x, cartesian_y = [coordinate / self.unit_offset for coordinate in coordinates]
        cartesian_y = -cartesian_y  #  flipped to negative IDK how but this actually works? TODO figure out why this works

        x_additive = (self.x_ticks_amount - 1) / 2  # Additives remove negatives on the number line
        y_additive = (self.y_ticks_amount - 1) / 2
        cartesian_x += x_additive
        cartesian_y += y_additive

        # Calculating how long would one "tick"
        x_tick_length = self.master.WIDTH / (self.x_ticks_amount - 1)
        y_tick_length = self.master.HEIGHT / (self.y_ticks_amount - 1)

        print((cartesian_x - x_additive) * x_tick_length, (cartesian_y - y_additive) * y_tick_length)
        return (cartesian_x * x_tick_length, cartesian_y * y_tick_length)

    def draw(self, gradient, y_intercept):
        # Resetting function
        self.remove(self.function_line)

        # Getting first 2 points base coordinates (x-intercept and y-intercept)
        limiting_y = (self.y_ticks_amount - 1) / 2
        limiting_point_1 = ((limiting_y - y_intercept) / gradient, limiting_y)
        limiting_point_2 = ((-limiting_y - y_intercept) / gradient, -limiting_y)

        # Getting coordinates relative to the window
        point_1_relative_coordinates, point_2_relative_coordinates = \
            [self.get_relative_coordinates(x) for x in (limiting_point_1,
                                                        limiting_point_2)]
        # Drawing out new points
        self.function_line = self.create_line(*point_1_relative_coordinates, *point_2_relative_coordinates, width=2)
        self.tag_raise(self.function_line)
