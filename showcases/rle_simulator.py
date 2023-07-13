# Imports
from showcase_template import ShowcaseTemplate


# Meta
MODULE_NAME = "Run-length encoding simulator"
MODULE_AUTHOR = "R1DF"
MODULE_DESCRIPTION = "This showcase allows the user to fill out a group of data and show how the RLE\n" \
                     "algorithm would encode the message."


#  Canvas class (must be named as Showcase)
class Showcase(ShowcaseTemplate):
    def __init__(self, master):
        # Inheritance
        super().__init__(master)
        self.config(bg="white")

        # Showcase attributes
        self.create_text(
            self.master.WIDTH // 2,
            30,
            text="Run-length encoding algorithm displayer"
        )

        # Creating grid with text
        self.BOX_LENGTH = 60
        self.BOX_AMOUNT = 5
        self.GRID_POSITION_X_OFFSET = 30
        self.GRID_POSITION_Y_OFFSET = 60
        self.rle_boxes = []
        self.rle_labels = []

        for y in range(self.BOX_AMOUNT):
            for x in range(self.BOX_AMOUNT):
                self.rle_boxes.append(self.create_rectangle(
                    (x * self.BOX_LENGTH) + self.GRID_POSITION_X_OFFSET,
                    (y * self.BOX_LENGTH) + self.GRID_POSITION_Y_OFFSET,
                    (x * self.BOX_LENGTH) + self.BOX_LENGTH + self.GRID_POSITION_X_OFFSET,
                    (y * self.BOX_LENGTH) + self.BOX_LENGTH + self.GRID_POSITION_Y_OFFSET,
                    outline="black"
                ))
                self.rle_labels.append(self.create_text(
                    (x * self.BOX_LENGTH) + self.GRID_POSITION_X_OFFSET + (self.BOX_LENGTH / 2),
                    (y * self.BOX_LENGTH) + self.GRID_POSITION_Y_OFFSET + (self.BOX_LENGTH / 2),
                    text=""
                ))

        # Creating description text
        self.create_text(
            (self.master.WIDTH / 2) + 165,
            (self.master.HEIGHT / 2) - 80,
            text=f"Enter any piece of text in the {self.BOX_AMOUNT}x{self.BOX_AMOUNT} grid\n"
                 f"and hit the \"Compress\" button below to\n"
                 f"view how the RLE algorithm would\n"
                 f"compress it.",
            justify="center",
            font="Arial 14"
        )

        # Creating button
        self.compress_button = {
            "rect": self.create_rectangle(
                (self.master.WIDTH / 2) + 50,
                (self.master.HEIGHT / 2) - 30,
                (self.master.WIDTH / 2) + 280,
                (self.master.HEIGHT / 2) + 40,
                width=2
            ),
            "text": self.create_text(
                (self.master.WIDTH / 2) + 165,
                (self.master.HEIGHT / 2) + 5,
                text="Compress"
            )
        }

        # Handling motion
        self.bind("<Motion>", self.handle_motion, add="+")

    def handle_motion(self, event):
        compress_box_coordinates = self.bbox(self.compress_button["rect"])
        if compress_box_coordinates[0] < event.x < compress_box_coordinates[2] and compress_box_coordinates[
            1] < event.y < compress_box_coordinates[3]:
            self.itemconfig(self.compress_button["rect"], fill="gray")
            return
        else:
            self.itemconfig(self.compress_button["rect"], fill="white")

        for box in self.rle_boxes:
            box_coordinates = self.bbox(box)
            if box_coordinates[0] < event.x < box_coordinates[2] and box_coordinates[1] < event.y < box_coordinates[3]:
                self.itemconfig(box, fill="gray")
            else:
                self.itemconfig(box, fill="white")

