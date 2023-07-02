# Imports
from tkinter import Toplevel, Label, Entry, Button
from .showcase_template import ShowcaseTemplate

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
        linear_function_input = self.linear_function_entry.get().strip().replace(" ", "")  # No spaces!

        # Viewing
        if not (linear_function_input.startswith("y=") or linear_function_input.startswith("f(x)=")):
            self.details_label.config(text="Invalid input!", fg="RED")
            return

        self.details_label.config(text=f"{linear_function_input} drawn successfully", fg="GREEN")


#  Canvas class (must be named as Showcase)
class Showcase(ShowcaseTemplate):
    def __init__(self, master):
        # Inheritance
        super().__init__(master)

        # Showcase attributes
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
        self.x_offset = 1
        self.y_offset = 1

        # Ensuring drawing out ticks is possible
        self.has_ticks = (self.master.WIDTH % 20 == 0) and (self.master.HEIGHT % 20 == 0)
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
                unit_shown = (self.x_ticks.index(tick) + 1) - x_mid_tick_value
                if unit_shown == 0:
                    continue  # No need to draw out 0

                tick_coordinates = self.bbox(tick)
                self.x_units.append([self.create_text(
                    tick_coordinates[2] - 2,
                    (self.master.HEIGHT // 2) + 13,
                    text=f"{unit_shown}",
                    font="Arial 10"
                ), unit_shown])  # [unit object, unit shown]

            y_mid_tick_value = len(self.y_ticks) // 2
            for tick in self.y_ticks:
                unit_shown = y_mid_tick_value - (self.y_ticks.index(tick) + 1)
                if unit_shown == 0:
                    continue  # No need to draw out 0

                tick_coordinates = self.bbox(tick)
                self.x_units.append([self.create_text(
                    (self.master.WIDTH // 2) + 13,
                    tick_coordinates[3] - 2,
                    text=f"{unit_shown}",
                    font="Arial 10"
                ), unit_shown])  # [unit object, unit shown]

        # Create toplevel
        self.function_inputter = FunctionInputter(self, self.master)

