"""This Python module contains the ShowcaseTemplate class that every Showcase class must inherit from.

Classes:
    ShowcaseTemplate: The parent class for every showcase that serves as a template."""

# Imports
from tkinter import Tk, Canvas


#  Canvas class (must be named as Showcase)
class ShowcaseTemplate(Canvas):
    def __init__(self, master: Tk):
        super().__init__(master)

    def remove(self, widget):
        if isinstance(widget, int):
            self.delete(widget)

    def end(self):
        self.master.handle_close()
