# Imports
from showcase_template import ShowcaseTemplate


# Meta
MODULE_NAME = "Distance between 2 points"
MODULE_AUTHOR = "R1DF"
MODULE_DESCRIPTION = "This showcase allows the user to click on 2 points on a window to calculate the distance\n" \
                     "between them using the Pythagorean theorem."


#  Canvas class (must be named as Showcase)
class Showcase(ShowcaseTemplate):
    def __init__(self, master):
        # Inheritance
        super().__init__(master)

        # Showcase attributes
        self.points = []
        self.coordinates = []
        self.connector = None
        self.description = None

        # Showcase constants
        self.POINT_SIZE = 4  # Best to be even

        # Binding
        self.bind("<Button-1>", self.handle_left_click, add="+")

    # Showcase-specific methods
    def create_connector(self):
        self.connector = self.create_line(*self.coordinates[0], *self.coordinates[1], fill="RED")
        dx = abs(self.coordinates[0][0] - self.coordinates[1][0])
        dy = abs(self.coordinates[0][1] - self.coordinates[1][1])
        distance = round(((dx ** 2) + (dy ** 2)) ** 0.5, 4)
        self.description = self.create_text(
            self.master.WIDTH - 100,
            self.master.HEIGHT - 30,
            text=f"Point 1: {self.coordinates[0]}\nPoint 2: {self.coordinates[1]}\nDistance: {distance} units",
            fill="RED"
        )

    # Bind handlers
    def handle_left_click(self, event):
        number_of_points = len(self.points)
        if number_of_points != 2:
            self.points.append(self.create_rectangle(
                event.x - (self.POINT_SIZE / 2),
                event.y - (self.POINT_SIZE / 2),
                event.x + (self.POINT_SIZE / 2),
                event.y + (self.POINT_SIZE / 2),
                fill="BLACK"
            ))
            self.coordinates.append((event.x, event.y))

            if number_of_points == 1:  # number_of_points BEFORE the new point!
                self.create_connector()

        else:
            for point in self.points:
                self.delete(point)
            self.remove(self.connector)
            self.remove(self.description)
            self.points = []
            self.coordinates = []
