# Imports
from showcase_template import ShowcaseTemplate
from tkinter import Toplevel, Label, Button, Entry, Frame, OptionMenu, StringVar


# Meta
MODULE_NAME = "Free body diagram on an object"
MODULE_AUTHOR = "R1DF"
MODULE_DESCRIPTION = "This showcase allows the user to control a free body diagram of an object and add forces\n" \
                     "to it, making some calculations as a result."

# Force adder
class ForceAdderToplevel(Toplevel):
    def __init__(self, master, master_showcase):
        self.master = master
        self.master_showcase = master_showcase
        super().__init__(self.master)
        self.title("Add force")
        self.resizable(False, False)

        # Getting directions
        self.directions = []
        if len(self.master_showcase.upward_forces) < 4:
            self.directions.append("Up")

        if len(self.master_showcase.downward_forces) < 4:
            self.directions.append("Down")

        if len(self.master_showcase.rightward_forces) < 4:
            self.directions.append("Right")

        if len(self.master_showcase.leftward_forces) < 4:
            self.directions.append("Left")

        # Setting up widgets
        self.introduction_label = Label(self, text="Select force details:")
        self.introduction_label.pack()

        self.details_frame = Frame(self)
        self.details_frame.pack()

        self.direction_label = Label(self.details_frame, text="Direction:")
        self.direction_label.grid(row=0, column=0)

        self.direction_stringvar = StringVar(self)
        self.direction_stringvar.set("Select from below")

        self.direction_optionmenu = OptionMenu(self.details_frame, self.direction_stringvar, *self.directions)
        self.direction_optionmenu.grid(row=0, column=1)

        self.direction_label = Label(self.details_frame, text="Magnitude in Newtons:")
        self.direction_label.grid(row=1, column=0)

        self.direction_entry = Entry(self.details_frame)
        self.direction_entry.grid(row=1, column=1)

        self.add_button = Button(self, text="Add", command=self.add_force)
        self.add_button.pack()

        # Protocol
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

    def handle_close(self):
        self.master_showcase.force_adder_toplevel = None
        self.destroy()

    def add_force(self):
        self.handle_close()

#  Canvas class (must be named as Showcase)
class Showcase(ShowcaseTemplate):
    def __init__(self, master):
        # Inheritance
        super().__init__(master)

        # Showcase attributes
        self.BOX_WIDTH = 300
        self.BOX_HEIGHT = 100
        self.object = self.create_rectangle(
            (self.master.WIDTH - self.BOX_WIDTH) // 2,
            (self.master.HEIGHT - self.BOX_HEIGHT) // 2,
            (self.master.WIDTH + self.BOX_WIDTH) // 2,
            (self.master.HEIGHT + self.BOX_HEIGHT) // 2,
            width=3
        )
        self.force_adder_toplevel = None
        self.upward_forces = []
        self.downward_forces = []
        self.rightward_forces = []
        self.leftward_forces = []

        self.add_force_box = {
            "rect": self.create_rectangle(
                (self.master.WIDTH // 2) - 100,
                self.master.HEIGHT - 50,
                (self.master.WIDTH // 2) + 100,
                self.master.HEIGHT - 20,
                width=2
            ),
            "text": self.create_text(
                self.master.WIDTH // 2,
                self.master.HEIGHT - 35,
                text="Add Force"
            )
        }

        # Bindings
        self.bind("<Motion>", self.handle_cursor_move, add="+")
        self.bind("<Button-1>", self.handle_cursor_lclick, add="+")

    def handle_cursor_move(self, event):
        box_coordinates = self.bbox(self.add_force_box["rect"])
        if box_coordinates[0] <= event.x <= box_coordinates[2] and box_coordinates[1] <= event.y <= box_coordinates[3]:
            self.itemconfig(self.add_force_box["rect"], fill="gray")
        else:
            self.itemconfig(self.add_force_box["rect"], fill="white")
    def handle_cursor_lclick(self, event):
        box_coordinates = self.bbox(self.add_force_box["rect"])
        if box_coordinates[0] <= event.x <= box_coordinates[2] and box_coordinates[1] <= event.y <= box_coordinates[3]:
            if self.force_adder_toplevel is None and any([len(x) < 4 for x in [self.upward_forces, self.downward_forces, self.rightward_forces, self.leftward_forces]]):
                self.force_adder_toplevel = ForceAdderToplevel(self.master, self)