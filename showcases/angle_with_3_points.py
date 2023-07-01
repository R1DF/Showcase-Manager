# Imports
from .showcase_template import ShowcaseTemplate
from math import copysign, acos, degrees, pi

# Meta
MODULE_NAME = "Constructing an angle and calculating it"
MODULE_AUTHOR = "R1DF"


#  Canvas class (must be named as Showcase)
class Showcase(ShowcaseTemplate):
    def __init__(self, master):
        # Inheritance
        super().__init__(master)

        # Showcase attributes
        self.orient_point = None
        self.orient_point_coordinates = []
        self.angle_points = []
        self.angle_points_coordinates = []
        self.angle_lines = []
        self.angle_text = None
        self.angle_description_text = None
        self.angle_arc = None

        # Showcase constants
        self.POINT_SIZE = 2  # Best to be even
        self.ANGLE_PRECISION_CONSTANT = 2  # How many d.p. of accuracy for angles?

        # Binding
        self.bind("<Button-1>", self.handle_left_click, add="+")

    # Showcase-specific methods
    def draw_description(self, angle_radians, angle_degrees):
        self.angle_text = self.create_text(
            self.master.WIDTH // 2,
            self.master.HEIGHT - 40,
            text=f"The angle is {angle_degrees}\u00b0 / {angle_radians} rad."
        )
        if angle_degrees == 0:
            angle_type = "zero"
        elif 90 > angle_degrees:
            angle_type = "acute"
        elif angle_degrees == 90:
            angle_type = "right"
        elif 180 > angle_degrees:
            angle_type = "obtuse"
        elif angle_degrees == 180:
            angle_type = "straight line"
        else:
            angle_type = "reflex"

        self.angle_description_text = self.create_text(
            self.master.WIDTH // 2,
            self.master.HEIGHT - 20,
            text=f"Angle type: {angle_type}."
        )

        # Creating arc
        self.angle_arc = self.create_arc(
            15,
            15,
            65,
            65,
            extent=angle_degrees
        )

    def calculate_angle(self):
        # Draw the lines between the orient point and the two angle points
        for angle_points_coordinates in self.angle_points_coordinates:
            self.angle_lines.append(self.create_line(
                *self.orient_point_coordinates,
                *angle_points_coordinates,
                fill="RED"
            ))

        # Figure out coordinates with respect to orient for angle points 1 and 2
        relative_coordinates_1 = [self.angle_points_coordinates[0][0] - self.orient_point_coordinates[0],
                                  self.orient_point_coordinates[1] - self.angle_points_coordinates[0][1]]
        relative_coordinates_2 = [self.angle_points_coordinates[1][0] - self.orient_point_coordinates[0],
                                  self.orient_point_coordinates[1] - self.angle_points_coordinates[1][1]]

        # Figure out quadrants that the orients are stuck in and the quadrant difference for angle points 1 and 2
        angle_points_quadrants = self.calculate_quadrants(relative_coordinates_1, relative_coordinates_2)
        quadrant_difference = abs(angle_points_quadrants[0] - angle_points_quadrants[1])

        # Using the law of cosines
        dx = abs(relative_coordinates_1[0] - relative_coordinates_2[0])
        dy = abs(relative_coordinates_1[1] - relative_coordinates_2[1])
        distance_by_angle_point_1 = round(
            ((relative_coordinates_1[0] ** 2) + (relative_coordinates_1[1] ** 2)) ** 0.5, 4)
        distance_by_angle_point_2 = round(
            ((relative_coordinates_2[0] ** 2) + (relative_coordinates_2[1] ** 2)) ** 0.5, 4)
        distance_between_angle_points = round(((dx ** 2) + (dy ** 2)) ** 0.5, 4)
        try:
            angle_radians = round(acos(
                ((distance_by_angle_point_1 ** 2) + (distance_by_angle_point_2 ** 2) - (
                            distance_between_angle_points ** 2)) /
                (2 * distance_by_angle_point_1 * distance_by_angle_point_2)
            ), self.ANGLE_PRECISION_CONSTANT)
            angle_degrees = round(degrees(angle_radians), self.ANGLE_PRECISION_CONSTANT)
        except ZeroDivisionError:
            self.angle_description_text = self.create_text(
                self.master.WIDTH // 2,
                self.master.HEIGHT - 40,
                text="Please make a valid angle."
            )
            return

        if quadrant_difference >= 2 or (
                quadrant_difference == 0 and relative_coordinates_2[1] < relative_coordinates_1[1] and
                relative_coordinates_1[0] > 0):
            angle_radians = pi - angle_radians
            angle_degrees = 360 - angle_degrees

        self.draw_description(angle_radians, angle_degrees)

    def calculate_quadrants(self, *coordinates):
        quadrants = []
        for coordinate_set in coordinates:
            signs = [copysign(1, x) for x in coordinate_set]
            match signs:
                case [1.0, 1.0]:
                    quadrants.append(1)
                case [-1.0, 1.0]:
                    quadrants.append(2)
                case [-1.0, -1.0]:
                    quadrants.append(3)
                case [1.0, -1.0]:
                    quadrants.append(4)
        return quadrants

    # Bind handlers
    def handle_left_click(self, event):
        if self.orient_point is None:
            self.orient_point = self.create_rectangle(
                event.x - (self.POINT_SIZE / 2),
                event.y - (self.POINT_SIZE / 2),
                event.x + (self.POINT_SIZE / 2),
                event.y + (self.POINT_SIZE / 2),
                fill="BLACK"
            )
            self.orient_point_coordinates = [event.x, event.y]

        elif len(self.angle_points) <= 1:
            self.angle_points.append(self.create_rectangle(
                event.x - (self.POINT_SIZE / 2),
                event.y - (self.POINT_SIZE / 2),
                event.x + (self.POINT_SIZE / 2),
                event.y + (self.POINT_SIZE / 2),
                fill="RED"
            ))
            self.angle_points_coordinates.append([event.x, event.y])

            if len(self.angle_points) == 2:
                self.calculate_angle()

        else:
            self.remove(self.orient_point)
            for angle_point in self.angle_points:
                self.remove(angle_point)
            for angle_line in self.angle_lines:
                self.remove(angle_line)
            self.remove(self.angle_text)
            self.remove((self.angle_description_text))
            self.remove(self.angle_arc)
            self.orient_point, self.angle_points, self.angle_lines = None, [], []
            self.angle_points_coordinates, self.orient_point_coordinates = [], []
