from py3d.core_ext.mesh import Mesh
from py3d.geometry.geometry import Geometry
from py3d.material.line import LineMaterial


class GridHelper(Mesh):
    def __init__(self, size=10, divisions=10, grid_color=(0, 0, 0), center_color=(0.5, 0.5, 0.5), line_width=1):
        geometry = Geometry()
        position_data = []
        color_data = []
        # Create range of values
        values = []
        delta_size = size / divisions
        for n in range(divisions + 1):
            values.append(-size / 2 + n * delta_size)
        # Add vertical lines
        for x in values:
            position_data.append([x, -size / 2, 0])
            position_data.append([x, size / 2, 0])
            if x == 0:
                color_data.append(center_color)
                color_data.append(center_color)
            else:
                color_data.append(grid_color)
                color_data.append(grid_color)
        # Add horizontal lines
        for y in values:
            position_data.append([-size / 2, y, 0])
            position_data.append([size / 2, y, 0])
            if y == 0:
                color_data.append(center_color)
                color_data.append(center_color)
            else:
                color_data.append(grid_color)
                color_data.append(grid_color)
        geometry.add_attribute("vec3", "vertexPosition", position_data)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = LineMaterial(
            property_dict = {
                "useVertexColors": 1,
                "lineWidth": line_width,
                "lineType": "segments"
            }
        )
        # Initialize the mesh
        super().__init__(geometry, material)
