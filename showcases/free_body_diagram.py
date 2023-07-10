# Imports
from showcase_template import ShowcaseTemplate


# Meta
MODULE_NAME = "Free body diagram on an object"
MODULE_AUTHOR = "R1DF"
MODULE_DESCRIPTION = "This showcase allows the user to control a free body diagram of an object and add forces\n" \
                     "to it, making some calculations as a result."


#  Canvas class (must be named as Showcase)
class Showcase(ShowcaseTemplate):
    def __init__(self, master):
        # Inheritance
        super().__init__(master)

        # Showcase attributes

