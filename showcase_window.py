# Imports
from tkinter import Tk


# Window class
class Window(Tk):
    def __init__(self, showcase_module=None):
        # Setup
        super().__init__()
        self.title("Physics Showcase")
        self.WIDTH, self.HEIGHT = 600, 400
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(False, False)
        self.config(bg="GRAY")

        # Adding showcase from module
        self.showcase = showcase_module.Showcase(self)
        self.showcase.pack(expand=1, fill="both")

