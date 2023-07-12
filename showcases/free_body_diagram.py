# Imports
from showcase_template import ShowcaseTemplate
from tkinter import Toplevel, Label, Button, Entry, Frame, OptionMenu, StringVar, messagebox


# Meta
MODULE_NAME = "Free body diagram on an object"
MODULE_AUTHOR = "R1DF"
MODULE_DESCRIPTION = "This showcase allows the user to control a free body diagram of an object and add forces\n" \
                     "to it, making some calculations as a result."

# Box mass setter
class BoxMassSetterToplevel(Toplevel):
    def __init__(self, master, master_showcase):
        self.master = master
        self.master_showcase = master_showcase
        super().__init__(self.master)
        self.title("Set box mass")
        self.resizable(False, False)

        # Setting up widgets
        self.introduction_label = Label(self, text="Mass in kilograms:")
        self.introduction_label.pack()

        self.mass_entry = Entry(self)
        self.mass_entry.pack()

        self.set_button = Button(self, text="Done", command=self.set_mass)
        self.set_button.pack()

        # Protocol
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

    def set_mass(self):
        mass_str = self.mass_entry.get().strip()
        if not mass_str.isnumeric():
            messagebox.showerror("Error", "Please enter a numeric value for the mass.")
            return
        self.master_showcase.configure_mass(int(mass_str))
        self.handle_close()

    def handle_close(self):
        self.master_showcase.box_mass_setter_toplevel = None
        self.destroy()

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
        if len(self.master_showcase.forces["Up"]) < 3:
            self.directions.append("Up")

        if len(self.master_showcase.forces["Down"]) < 3:
            self.directions.append("Down")

        if len(self.master_showcase.forces["Right"]) < 3:
            self.directions.append("Right")

        if len(self.master_showcase.forces["Left"]) < 3:
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

        self.magnitude_label = Label(self.details_frame, text="Magnitude in Newtons:")
        self.magnitude_label.grid(row=1, column=0)

        self.magnitude_entry = Entry(self.details_frame)
        self.magnitude_entry.grid(row=1, column=1)

        self.add_button = Button(self, text="Add", command=self.add_force)
        self.add_button.pack()

        # Protocol
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

    def handle_close(self):
        self.master_showcase.force_adder_toplevel = None
        self.destroy()

    def add_force(self):
        direction = self.direction_stringvar.get()
        magnitude_str = self.magnitude_entry.get().strip()
        if direction == "Select from below":
            messagebox.showerror("Error", "Please select a direction.")
            return

        if not magnitude_str.isnumeric():
            messagebox.showerror("Error", "Please enter a numerical value for the force.")
            return

        magnitude = int(magnitude_str)
        if not magnitude:
            messagebox.showerror("Error", "Force cannot be 0N.")
            return

        self.master_showcase.add_force(direction, magnitude)
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
        self.mass_label = self.create_text(
            self.master.WIDTH // 2,
            self.master.HEIGHT // 2,
            text=""
        )
        self.force_adder_toplevel = None
        self.forces = {"Up": [], "Down": [], "Right": [], "Left": []}
        self.force_arrows = {"Up": [], "Down": [], "Right": [], "Left": []}
        self.force_scales = {"Up": [], "Down": [], "Right": [], "Left": []}
        self.box_mass_setter_toplevel = None
        self.object_mass = None

        self.add_force_box = {
            "rect": self.create_rectangle(
                20,
                self.master.HEIGHT - 35,
                170,
                self.master.HEIGHT - 5,
                width=2
            ),
            "text": self.create_text(
                95,
                self.master.HEIGHT - 20,
                text="Add Force"
            )
        }

        self.set_box_mass_box = {
            "rect": self.create_rectangle(
                self.master.WIDTH - 170,
                self.master.HEIGHT - 35,
                self.master.WIDTH - 20,
                self.master.HEIGHT - 5,
                width=2
            ),
            "text": self.create_text(
                self.master.WIDTH - 95,
                self.master.HEIGHT - 20,
                text="Set Box Mass"
            )
        }

        # Bindings
        self.bind("<Motion>", self.handle_cursor_move, add="+")
        self.bind("<Button-1>", self.handle_cursor_lclick, add="+")

    def handle_cursor_move(self, event):
        add_force_box_coordinates = self.bbox(self.add_force_box["rect"])
        mass_setter_box_coordinates = self.bbox(self.set_box_mass_box["rect"])
        if add_force_box_coordinates[0] <= event.x <= add_force_box_coordinates[2] and add_force_box_coordinates[1] <= event.y <= add_force_box_coordinates[3]:
            self.itemconfig(self.add_force_box["rect"], fill="gray")
            self.itemconfig(self.set_box_mass_box["rect"], fill="white")
        elif mass_setter_box_coordinates[0] <= event.x <= mass_setter_box_coordinates[2] and mass_setter_box_coordinates[1] <= event.y <= mass_setter_box_coordinates[3]:
            self.itemconfig(self.add_force_box["rect"], fill="white")
            self.itemconfig(self.set_box_mass_box["rect"], fill="gray")
        else:
            self.itemconfig(self.add_force_box["rect"], fill="white")
            self.itemconfig(self.set_box_mass_box["rect"], fill="white")
    def handle_cursor_lclick(self, event):
        add_force_box_coordinates = self.bbox(self.add_force_box["rect"])
        mass_setter_box_coordinates = self.bbox(self.set_box_mass_box["rect"])
        if add_force_box_coordinates[0] <= event.x <= add_force_box_coordinates[2] and add_force_box_coordinates[1] <= event.y <= add_force_box_coordinates[3]:
            if self.force_adder_toplevel is None and any([len(x) < 4 for x in self.forces.values()]):
                self.force_adder_toplevel = ForceAdderToplevel(self.master, self)
        elif mass_setter_box_coordinates[0] <= event.x <= mass_setter_box_coordinates[2] and mass_setter_box_coordinates[1] <= event.y <= mass_setter_box_coordinates[3]:
            if self.box_mass_setter_toplevel is None:
                self.box_mass_setter_toplevel = BoxMassSetterToplevel(self.master, self)

    def add_force(self, direction, magnitude):
        # Adding force magnitude
        self.forces[direction].append(magnitude)
        offset_multiple_index = len(self.forces[direction]) - 1
        object_coordinates = self.bbox(self.object)

        # Drawing the force
        match direction:
            case "Up":
                self.force_arrows[direction].append(self.create_line(
                    ((object_coordinates[0] + object_coordinates[2]) / 2) + (70 * [0, -1, 1][offset_multiple_index]),
                    object_coordinates[1] - 20,
                    ((object_coordinates[0] + object_coordinates[2]) / 2) + (70 * [0, -1, 1][offset_multiple_index]),
                    object_coordinates[1] - 80,
                    width=4,
                    arrow="last"
                ))
                self.force_scales[direction].append(self.create_text(
                    ((object_coordinates[0] + object_coordinates[2]) / 2) + (70 * [0, -1, 1][offset_multiple_index]),
                    object_coordinates[1] - 90,
                    text=f"{magnitude}N"
                ))

            case "Down":
                self.force_arrows[direction].append(self.create_line(
                    ((object_coordinates[0] + object_coordinates[2]) / 2) + (70 * [0, -1, 1][offset_multiple_index]),
                    object_coordinates[3] + 20,
                    ((object_coordinates[0] + object_coordinates[2]) / 2) + (70 * [0, -1, 1][offset_multiple_index]),
                    object_coordinates[3] + 80,
                    width=4,
                    arrow="last"
                ))
                self.force_scales[direction].append(self.create_text(
                    ((object_coordinates[0] + object_coordinates[2]) / 2) + (70 * [0, -1, 1][offset_multiple_index]),
                    object_coordinates[3] + 100,
                    text=f"{magnitude}N"
                ))

            case "Right":
                self.force_arrows[direction].append(self.create_line(
                    object_coordinates[2] + 20,
                    ((object_coordinates[1] + object_coordinates[3]) / 2) + (40 * [0, -1, 1][offset_multiple_index]),
                    object_coordinates[2] + 80,
                    ((object_coordinates[1] + object_coordinates[3]) / 2) + (40 * [0, -1, 1][offset_multiple_index]),
                    width=4,
                    arrow="last"
                ))
                self.force_scales[direction].append(self.create_text(
                    object_coordinates[2] + 100,
                    ((object_coordinates[1] + object_coordinates[3]) / 2) + (40 * [0, -1, 1][offset_multiple_index]),
                    text=f"{magnitude}N"
                ))

            case "Left":
                self.force_arrows[direction].append(self.create_line(
                    object_coordinates[0] - 20,
                    ((object_coordinates[1] + object_coordinates[3]) / 2) + (40 * [0, -1, 1][offset_multiple_index]),
                    object_coordinates[0] - 80,
                    ((object_coordinates[1] + object_coordinates[3]) / 2) + (40 * [0, -1, 1][offset_multiple_index]),
                    width=4,
                    arrow="last"
                ))
                self.force_scales[direction].append(self.create_text(
                    object_coordinates[0] - 100,
                    ((object_coordinates[1] + object_coordinates[3]) / 2) + (40 * [0, -1, 1][offset_multiple_index]),
                    text=f"{magnitude}N"
                ))

    def configure_mass(self, mass):
        self.object_mass = mass
        self.itemconfig(self.mass_label, text=f"{mass}kg")
        self.make_calculations()

    def make_calculations(self):
        pass
