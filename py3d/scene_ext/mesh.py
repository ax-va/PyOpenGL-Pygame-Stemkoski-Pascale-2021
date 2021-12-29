import OpenGL.GL as GL

from py3d.scene_ext.object_3d import Object3D


class Mesh(Object3D):
    """
    Contains geometric data that specifes vertex-related properties and material data
    that specifes the general appearance of the object
    """
    def __init__(self, geometry, material):
        super().__init__()
        self._geometry = geometry
        self._material = material
        # Should this object be rendered?
        self._visible = True
        # Set up associations between attributes stored in geometry
        # and shader program stored in material
        self._vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_ref)
        for variable_name, attribute_object in geometry.attributes.items():
            attribute_object.associate_variable(material.program_ref, variable_name)
        # Unbind this vertex array object
        GL.glBindVertexArray(0)