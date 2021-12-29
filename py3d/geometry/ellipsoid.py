from math import sin, cos, pi

from py3d.geometry.geometry import ParametricGeometry


class EllipsoidGeometry(ParametricGeometry):
    def __init__(self, width=1, height=1, depth=1, radius_segments=32, height_segments=16):
        # [x, y, z] = surface_function(u, v)
        def surface_function(u, v):
            return [width / 2 * sin(u) * cos(v),
                    height / 2 * sin(v),
                    depth / 2 * cos(u) * cos(v)]

        super().__init__(0, 2*pi, radius_segments,
                         -pi/2, pi/2, height_segments,
                         surface_function)