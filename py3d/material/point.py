import OpenGL.GL as GL

from py3d.material.basic import BasicMaterial


class PointMaterial(BasicMaterial):
    def __init__(self, vertex_shader_code=None, fragment_shader_code=None, property_dict=None, use_vertex_colors=True):
        super().__init__(vertex_shader_code, fragment_shader_code, use_vertex_colors)
        # Render vertices as points
        self._setting_dict["drawStyle"] = GL.GL_POINTS
        # Set the width and height of points, in pixels
        self._setting_dict["pointSize"] = 8
        # Draw points as rounded
        self._setting_dict["roundedPoints"] = False
        self.set_properties(property_dict)

    def update_render_settings(self):
        GL.glPointSize(self._setting_dict["pointSize"])
        if self._setting_dict["roundedPoints"]:
            GL.glEnable(GL.GL_POINT_SMOOTH)
        else:
            GL.glDisable(GL.GL_POINT_SMOOTH)
