from math import sin, cos, pi

from py3d.geometry.geometry import Geometry


class PolygonGeometry(Geometry):
    def __init__(self, sides=3, radius=1):
        sides = int(sides)
        if sides < 3:
            raise ValueError(f"the 'sides' parameter must be at least three")
        super().__init__()
        a = 2 * pi / sides
        position_data = []
        color_data = []
        uv_data = []
        uv_center = [0.5, 0.5]
        for n in range(sides):
            position_data.append([0, 0, 0])
            position_data.append([radius * cos(n * a), radius * sin(n * a), 0])
            position_data.append([radius * cos((n + 1) * a), radius * sin((n + 1) * a), 0])
            color_data.append([1, 1, 1])
            color_data.append([1, 0, 0])
            color_data.append([0, 0, 1])
            uv_data.append(uv_center)
            uv_data.append([cos(n * a) * 0.5 + 0.5, sin(n * a) * 0.5 + 0.5])
            uv_data.append([cos((n + 1) * a) * 0.5 + 0.5, sin((n + 1) * a) * 0.5 + 0.5])
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.count_vertices()

    @staticmethod
    def create_triangle_geometry(radius=1):
        return PolygonGeometry(sides=3, radius=radius)

    @staticmethod
    def create_square_geometry(radius=1):
        return PolygonGeometry(sides=4, radius=radius)

    @staticmethod
    def create_pentagon_geometry(radius=1):
        return PolygonGeometry(sides=5, radius=radius)

    @staticmethod
    def create_hexagon_geometry(radius=1):
        return PolygonGeometry(sides=6, radius=radius)