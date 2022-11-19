import OpenGL.GL as GL

from py3d.material.material import Material


class TextureMaterial(Material):
    def __init__(self, texture, property_dict=None):
        vertex_shader_code = """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec2 vertexUV;
            uniform vec2 repeatUV;
            uniform vec2 offsetUV;
            out vec2 UV;
            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                UV = vertexUV * repeatUV + offsetUV;
            }
        """

        fragment_shader_code = """
            uniform vec3 baseColor;
            uniform sampler2D textureSampler;
            in vec2 UV;
            out vec4 fragColor;
            void main()
            {
                vec4 color = vec4(baseColor, 1.0) * texture(textureSampler, UV);
                if (color.a < 0.1)
                    discard;                    
                fragColor = color;
            }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform("sampler2D", "textureSampler", [texture.texture_ref, 1])
        self.add_uniform("vec2", "repeatUV", [1.0, 1.0])
        self.add_uniform("vec2", "offsetUV", [0.0, 0.0])
        self.locate_uniforms()
        # Render both sides?
        self.setting_dict["doubleSide"] = True
        # Render triangles as wireframe?
        self.setting_dict["wireframe"] = False
        # line thickness for wireframe rendering
        self.setting_dict["lineWidth"] = 1
        self.set_properties(property_dict)

    def update_render_settings(self):
        if self.setting_dict["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
        if self.setting_dict["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glLineWidth(self.setting_dict["lineWidth"])
