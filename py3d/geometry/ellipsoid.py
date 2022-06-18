import math

from py3d.core.matrix import Matrix
from py3d.geometry.parametric import ParametricGeometry


class EllipsoidGeometry(ParametricGeometry):
    def __init__(self, width=1, height=1, depth=1, theta_segments=16, phi_segments=32):
        def surface_function(u, v):
            # [x, y, z] = surface_function(u, v)
            # Here,
            # x = width / 2 * sin(theta) * cos(phi),
            # y = height / 2 * sin(theta) * sin(phi),
            # z = depth / 2 * cos(theta),
            # where 0 <= theta < pi, 0 <= phi < 2*pi.
            # Then, u = phi / (2*pi), v = (1 - theta/pi).
            # Then, phi = 2 * pi * u, theta = (1 - v)*pi.
            phi = 2 * math.pi * u
            theta = (1 - v) * math.pi
            return [width / 2 * math.sin(theta) * math.cos(phi),
                    height / 2 * math.sin(theta) * math.sin(phi),
                    depth / 2 * math.cos(theta)]

        super().__init__(u_start=0,
                         u_end=1,
                         u_resolution=phi_segments,
                         v_start=0,
                         v_end=1,
                         v_resolution=theta_segments,
                         surface_function=surface_function)
        # Rotate the ellipsoid around the x-axis on -90 degrees.
        # The vertices and normals will be recalculated.
        self.apply_matrix(Matrix.make_rotation_x(-math.pi/2))
