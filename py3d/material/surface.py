import OpenGL.GL as GL

from py3d.material.basic import BasicMaterial


class SurfaceMaterial(BasicMaterial):
    def __init__(self, vertex_shader_code=None, fragment_shader_code=None, property_dict=None, use_vertex_colors=True):
        super().__init__(vertex_shader_code, fragment_shader_code, use_vertex_colors)
        # Render vertices as surface
        self._setting_dict["drawStyle"] = GL.GL_TRIANGLES
        # Render both sides? default: front side only
        # (vertices ordered counterclockwise)
        self._setting_dict["doubleSide"] = False
        # Render triangles as wireframe?
        self._setting_dict["wireframe"] = False
        # Set line thickness for wireframe rendering
        self._setting_dict["lineWidth"] = 1
        self.set_properties(property_dict)

    def update_render_settings(self):
        if self._setting_dict["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
        if self._setting_dict["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glLineWidth(self._setting_dict["lineWidth"])
