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

        # Showcase attributes

