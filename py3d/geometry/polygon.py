import math

from py3d.geometry.geometry import Geometry


class PolygonGeometry(Geometry):
    """ Symmetrical polygon inscribed in a circle """
    def __init__(self, sides=3, radius=1, normals_up=True):
        sides = int(sides)
        if sides < 3:
            raise ValueError(f"the 'sides' parameter must be at least three")
        super().__init__()
        delta_phi = 2 * math.pi / sides
        position_data = []
        color_data = []
        uv_data = []
        uv_center = [0.5, 0.5]
        normal_data = []
        normal_vector = [0, 0, 1] if normals_up else [0, 0, -1]
        for n in range(sides):
            position_data.append([0, 0, 0])
            position_data.append([radius * math.cos(n * delta_phi), radius * math.sin(n * delta_phi), 0])
            position_data.append([radius * math.cos((n + 1) * delta_phi), radius * math.sin((n + 1) * delta_phi), 0])
            color_data.append([1, 1, 1])
            color_data.append([1, 0, 0])
            color_data.append([0, 0, 1])
            uv_data.append(uv_center)
            uv_data.append([math.cos(n * delta_phi) * 0.5 + 0.5, math.sin(n * delta_phi) * 0.5 + 0.5])
            uv_data.append([math.cos((n + 1) * delta_phi) * 0.5 + 0.5, math.sin((n + 1) * delta_phi) * 0.5 + 0.5])
            # Repeat three times for three vertices of triangle
            for i in range(3):
                normal_data.append(normal_vector.copy())
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.add_attribute("vec3", "vertexNormal", normal_data)
        self.add_attribute("vec3", "faceNormal", normal_data)

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