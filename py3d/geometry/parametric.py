from py3d.geometry.geometry import Geometry


class ParametricGeometry(Geometry):
    def __init__(self,
                 u_start, u_end, u_resolution,
                 v_start, v_end, v_resolution,
                 surface_function):
        # Generate set of points on function
        delta_u = (u_end - u_start) / u_resolution
        delta_v = (v_end - v_start) / v_resolution
        positions = []

        for u_index in range(u_resolution + 1):
            array = []
            for v_index in range(v_resolution + 1):
                u = u_start + u_index * delta_u
                v = v_start + v_index * delta_v
                array.append(surface_function(u, v))
            positions.append(array)

        # Store vertex data
        position_data = []
        color_data = []
        # default vertex colors
        c1, c2, c3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        c4, c5, c6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]

        # Group vertex data into triangles
        # Note: .copy() is necessary to avoid storing references
        for x_index in range(u_resolution):
            for y_index in range(v_resolution):
                # position data
                p0 = positions[x_index + 0][y_index + 0]
                p1 = positions[x_index + 1][y_index + 0]
                p3 = positions[x_index + 0][y_index + 1]
                p2 = positions[x_index + 1][y_index + 1]
                position_data += [p0.copy(), p1.copy(), p2.copy(),
                                  p0.copy(), p2.copy(), p3.copy()]
                # color data
                color_data += [c1, c2, c3, c4, c5, c6]

        self.add_attribute("vec3", "vertexPosition",  position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.count_vertices()