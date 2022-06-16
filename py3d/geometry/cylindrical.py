import math

from py3d.core.matrix import Matrix
from py3d.geometry.parametric import ParametricGeometry
from py3d.geometry.polygon import  PolygonGeometry


class CylindricalGeometry(ParametricGeometry):
    def __init__(self, radius_top=1, radius_bottom=1, height=1,
                 radial_segments=32, height_segments=4,
                 closed_top=True, closed_bottom=True):
        def surface_function(u, v):
            return [(v*radius_top + (1 - v)*radius_bottom)*math.sin(u),
                    height*(v - 0.5),
                    (v*radius_top + (1 - v)*radius_bottom)*math.cos(u)]
        super().__init__(0, 2*math.pi, radial_segments, 0, 1, height_segments, surface_function)

        if closed_top:
            top_geometry = PolygonGeometry(radial_segments, radius_top)
            transform = Matrix.make_translation(0, height/2, 0) \
                      @ Matrix.make_rotation_y(-math.pi/2) \
                      @ Matrix.make_rotation_x(-math.pi/2)
            top_geometry.apply_matrix(transform)
            self.merge(top_geometry)
        if closed_bottom:
            bottom_geometry = PolygonGeometry(radial_segments, radius_bottom)
            transform = Matrix.make_translation(0, -height/2, 0) \
                      @ Matrix.make_rotation_y(-math.pi/2) \
                      @ Matrix.make_rotation_x(-math.pi/2)
            bottom_geometry.apply_matrix(transform)
            self.merge(bottom_geometry)