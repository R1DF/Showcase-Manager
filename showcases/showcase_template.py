"""This Python module contains the ShowcaseTemplate class that every Showcase class must inherit from.

Classes:
    ShowcaseTemplate: The parent class for every showcase that serves as a template."""

# Imports
from tkinter import Tk, Canvas


#  Canvas class (must be named as Showcase)
class ShowcaseTemplate(Canvas):
    def __init__(self, master_window):
        self.master_window = master_window
        self.master_showcase = master_window.showcase_module
        super().__init__(self.master_window)

    def remove(self, widget):
        if isinstance(widget, int):
            self.delete(widget)

    def end(self):
        self.master.handle_close()
