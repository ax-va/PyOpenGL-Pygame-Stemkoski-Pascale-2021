import numpy

from numpy import subtract, divide, cross
from numpy.linalg import norm
from math import sin, cos, tan, pi


class Matrix:
    """
    Contains static methods to generate matrices (with the numpy library) corresponding
    to identity, translation, rotation (around each axis), scaling, and projection.
    """
    @staticmethod
    def make_identity():
        return numpy.array(
            [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]]
        ).astype(float)

    @staticmethod
    def make_translation(x, y, z):
        return numpy.array(
            [[1, 0, 0, x],
             [0, 1, 0, y],
             [0, 0, 1, z],
             [0, 0, 0, 1]]
        ).astype(float)

    @staticmethod
    def make_rotation_x(angle):
        c = cos(angle)
        s = sin(angle)
        return numpy.array(
            [[1,  0,  0,  0],
             [0,  c, -s,  0],
             [0,  s,  c,  0],
             [0,  0,  0,  1]]
        ).astype(float)

    @staticmethod
    def make_rotation_y(angle):
        c = cos(angle)
        s = sin(angle)
        return numpy.array(
            [[c,  0,  s,  0],
             [0,  1,  0,  0],
             [-s, 0,  c,  0],
             [0,  0,  0,  1]]
        ).astype(float)

    @staticmethod
    def make_rotation_z(angle):
        c = cos(angle)
        s = sin(angle)
        return numpy.array(
            [[c, -s,  0,  0],
             [s,  c,  0,  0],
             [0,  0,  1,  0],
             [0,  0,  0,  1]]
        ).astype(float)

    @staticmethod
    def make_scale(s):
        return numpy.array(
            [[s, 0, 0, 0],
             [0, s, 0, 0],
             [0, 0, s, 0],
             [0, 0, 0, 1]]
        ).astype(float)

    @staticmethod
    def make_perspective(angle_of_view=60, aspect_ratio=1, near=0.1, far=1000):
        a = angle_of_view * pi / 180.0
        d = 1.0 / tan(a / 2)
        b = (far + near) / (near - far)
        c = 2 * far * near / (near - far)
        return numpy.array(
            [[d / aspect_ratio, 0, 0, 0],
             [0, d, 0, 0],
             [0, 0, b, c],
             [0, 0, -1, 0]]
        ).astype(float)

    @staticmethod
    def make_look_at(position, target):
        world_up = [0, 1, 0]
        forward = subtract(target, position)
        right = cross(forward, world_up)
        # If forward and world_up vectors are parallel,
        # the right vector is zero.
        # Fix this by perturbing the world_up vector a bit
        if norm(right) < 0.001:
            offset = numpy.array([0.001, 0, 0])
            right = cross(forward, world_up + offset)
        up = cross(right, forward)
        # All vectors should have length 1
        forward = divide(forward, norm(forward))
        right = divide(right, norm(right))
        up = divide(up, norm(up))
        return numpy.array(
            [[right[0], up[0], -forward[0], position[0]],
             [right[1], up[1], -forward[1], position[1]],
             [right[2], up[2], -forward[2], position[2]],
             [0, 0, 0, 1]]
        )
