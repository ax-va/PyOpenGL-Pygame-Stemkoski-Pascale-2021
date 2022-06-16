import numpy as np
from py3d.geometry.geometry import Geometry


class ParametricGeometry(Geometry):
    """
    Parametric geometry defined by
    (x, y, z) = surface_function(u, v),
    where u and v are the parameters
    """
    def __init__(self,
                 u_start, u_end, u_resolution,
                 v_start, v_end, v_resolution,
                 surface_function):
        super().__init__()
        # Generate set of points on function
        delta_u = (u_end - u_start) / u_resolution
        delta_v = (v_end - v_start) / v_resolution

        position_list = []
        texture_position_list = []
        vertex_normal_list = []
        for u_index in range(u_resolution + 1):
            xyz_list = []
            uv_list = []
            n_list = []
            for v_index in range(v_resolution + 1):
                # 3D vertex coordinates
                u = u_start + u_index * delta_u
                v = v_start + v_index * delta_v
                p = surface_function(u, v)
                xyz_list.append(p)
                # 3D normal coordinates
                p1 = surface_function(u + delta_u/1e3, v)
                p2 = surface_function(u, v + delta_v/1e3)
                normal_vector = self.calculate_normal(p, p1, p2)
                n_list.append(normal_vector)
                # 2D texture coordinates
                u_texture = u_index / u_resolution
                v_texture = v_index / v_resolution
                uv_list.append([u_texture, v_texture])
            position_list.append(xyz_list)
            vertex_normal_list.append(n_list)
            texture_position_list.append(uv_list)

        # Store vertex data
        position_data = []
        color_data = []
        uv_data = []
        # default vertex colors
        c1, c2, c3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        c4, c5, c6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]
        vertex_normal_data = []
        face_normal_data = []

        # Group vertex data into triangles.
        # Note: .copy() is necessary to avoid storing references.
        # position_data will be also copied in apply_matrix() in the Geometry class.
        for i_index in range(u_resolution):
            for j_index in range(v_resolution):
                # position data
                p_a = position_list[i_index + 0][j_index + 0]
                p_b = position_list[i_index + 1][j_index + 0]
                p_c = position_list[i_index + 1][j_index + 1]
                p_d = position_list[i_index + 0][j_index + 1]
                position_data += [p_a.copy(), p_b.copy(), p_c.copy(),
                                  p_a.copy(), p_c.copy(), p_d.copy()]
                # color data
                color_data += [c1, c2, c3,
                               c4, c5, c6]
                # uv data of texture coordinates
                uv_a = texture_position_list[i_index + 0][j_index + 0]
                uv_b = texture_position_list[i_index + 1][j_index + 0]
                uv_c = texture_position_list[i_index + 1][j_index + 1]
                uv_d = texture_position_list[i_index + 0][j_index + 1]
                uv_data += [uv_a, uv_b, uv_c,
                            uv_a, uv_c, uv_d]
                # vertex normal vectors
                n_a = vertex_normal_list[i_index + 0][j_index + 0]
                n_b = vertex_normal_list[i_index + 1][j_index + 0]
                n_c = vertex_normal_list[i_index + 1][j_index + 1]
                n_d = vertex_normal_list[i_index + 0][j_index + 1]
                vertex_normal_data += [n_a.copy(), n_b.copy(), n_c.copy(),
                                       n_a.copy(), n_c.copy(), n_d.copy()]
                # face normal vectors
                fn0 = self.calculate_normal(p_a, p_b, p_c)
                fn1 = self.calculate_normal(p_a, p_c, p_d)
                face_normal_data += [fn0.copy(), fn0.copy(), fn0.copy(),
                                     fn1.copy(), fn1.copy(), fn1.copy()]

        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.add_attribute("vec3", "vertexNormal", vertex_normal_data)
        self.add_attribute("vec3", "faceNormal", face_normal_data)

    @staticmethod
    def calculate_normal(p0, p1, p2):
        v1 = np.array(p1) - np.array(p0)
        v2 = np.array(p2) - np.array(p0)
        orthogonal_vector = np.cross(v1, v2)
        norm = np.linalg.norm(orthogonal_vector)
        normal_vector = orthogonal_vector / norm if norm > 1e-6 \
            else np.array(p0) / np.linalg.norm(p0)
        return normal_vector
