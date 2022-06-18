import math

from py3d.core.matrix import Matrix
from py3d.geometry.parametric import ParametricGeometry
from py3d.geometry.polygon import PolygonGeometry


class CylindricalGeometry(ParametricGeometry):
    def __init__(self, radius_top=1, radius_bottom=1, height=1,
                 radial_segments=32, height_segments=16,
                 closed_top=True, closed_bottom=True):
        def surface_function(u, v):
            # x = radius * cos(phi),
            # y = radius * sin(phi),
            # z = z,
            # where 0 <= phi < 2*pi.
            # Then, u = phi / (2*pi), v = z.
            # Then, phi = 2 * pi * u, z = v.
            phi = 2 * math.pi * u
            return [(v*radius_top + (1 - v)*radius_bottom) * math.cos(phi),
                    (v*radius_top + (1 - v)*radius_bottom) * math.sin(phi),
                    height*(v - 0.5)]

        super().__init__(u_start=0,
                         u_end=1,
                         u_resolution=radial_segments,
                         v_start=0,
                         v_end=1,
                         v_resolution=height_segments,
                         surface_function=surface_function)

        if closed_top:
            top_geometry = PolygonGeometry(
                sides=radial_segments,
                radius=radius_top,
                normals_up=True
            )
            transform = Matrix.make_translation(0, 0, height/2)
            top_geometry.apply_matrix(transform)
            self.merge(top_geometry)

        if closed_bottom:
            bottom_geometry = PolygonGeometry(
                sides=radial_segments,
                radius=radius_bottom,
                normals_up=False
            )
            transform = Matrix.make_translation(0, 0, -height/2)
            bottom_geometry.apply_matrix(transform)
            self.merge(bottom_geometry)

        # Rotate around the x-axis on -90 degrees.
        # The vertices and normals will be recalculated.
        self.apply_matrix(Matrix.make_rotation_x(-math.pi/2))
