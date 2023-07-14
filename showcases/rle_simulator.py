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
        self.typing_active = False
        self.uncompressed_text = ""

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

        # Creating text widgets
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
        self.typing_active_text = self.create_text(
            (self.master.WIDTH / 2) + 165,
            (self.master.HEIGHT / 2) + 60,
            text=""
        )
        self.compressed_text_label = self.create_text(
            (self.master.WIDTH / 2) + 165,
            (self.master.HEIGHT / 2) + 105,
            text="",
            justify="center"
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
        self.bind("<Button-1>", self.handle_lclick, add="+")
        self.master.bind("<KeyPress>", self.handle_type, add="+")

    def get_compressed(self):
        # RLE loop
        tracked_letter = self.uncompressed_text[0]
        repeats_counter = 1
        total_counter = 1
        compressed_text = ""
        while total_counter < len(self.uncompressed_text):
            current_letter = self.uncompressed_text[total_counter]
            if current_letter != tracked_letter:
                compressed_text += f"{repeats_counter}{tracked_letter}"
                tracked_letter = current_letter
                repeats_counter = 0
            total_counter += 1
            repeats_counter += 1

        # Adding last part that went unnoticed in loop above and returning
        compressed_text += f"{repeats_counter}{tracked_letter}"
        return compressed_text

    def handle_lclick(self, event):
        if self.GRID_POSITION_X_OFFSET < event.x < self.BOX_AMOUNT * self.BOX_LENGTH + self.GRID_POSITION_X_OFFSET and \
                self.GRID_POSITION_Y_OFFSET < event.y < self.BOX_AMOUNT * self.BOX_LENGTH + self.GRID_POSITION_Y_OFFSET:
            self.typing_active = True
            self.itemconfig(self.typing_active_text, text="Key presses are being recorded")
        else:
            self.typing_active = False
            self.itemconfig(self.typing_active_text,
                            text="")

        compress_box_coordinates = self.bbox(self.compress_button["rect"])
        if compress_box_coordinates[0] < event.x < compress_box_coordinates[2] and compress_box_coordinates[
            1] < event.y < compress_box_coordinates[3]:
            if len(self.uncompressed_text):
                compressed_text = self.get_compressed()
                self.itemconfig(self.compressed_text_label, text=f"Uncompressed:\n{self.uncompressed_text}\nCompressed:\n{compressed_text}")
            else:
                self.itemconfig(self.compressed_text_label, text=f"")
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

    def handle_type(self, event):
        if not self.typing_active:
            return

        char = event.char
        if event.keysym == "BackSpace" and len(self.uncompressed_text):
            self.itemconfig(self.rle_labels[len(self.uncompressed_text) - 1], text="")
            self.uncompressed_text = self.uncompressed_text[:-1]

        elif char.isalpha() and len(self.uncompressed_text) != self.BOX_AMOUNT ** 2:
            self.itemconfig(self.rle_labels[len(self.uncompressed_text)], text=char)
            self.uncompressed_text += char
