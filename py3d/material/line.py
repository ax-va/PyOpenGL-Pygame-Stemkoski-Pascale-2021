import OpenGL.GL as GL

from py3d.material.basic import BasicMaterial


class LineMaterial(BasicMaterial):
    def __init__(self, vertex_shader_code=None, fragment_shader_code=None, property_dict=None, use_vertex_colors=True):
        super().__init__(vertex_shader_code, fragment_shader_code, use_vertex_colors)
        # Render vertices as continuous line by default
        self._setting_dict["drawStyle"] = GL.GL_LINE_STRIP
        # Set the line thickness
        self._setting_dict["lineWidth"] = 1
        # line type: "connected" | "loop" | "segments"
        self._setting_dict["lineType"] = "connected"
        self.set_properties(property_dict)

    def update_render_settings(self):
        GL.glLineWidth(self._setting_dict["lineWidth"])
        if self._setting_dict["lineType"] == "connected":
            self._setting_dict["drawStyle"] = GL.GL_LINE_STRIP
        elif self._setting_dict["lineType"] == "loop":
            self._setting_dict["drawStyle"] = GL.GL_LINE_LOOP
        elif self._setting_dict["lineType"] == "segments":
            self._setting_dict["drawStyle"] = GL.GL_LINES
        else:
            raise Exception("Unknown LineMaterial draw style")