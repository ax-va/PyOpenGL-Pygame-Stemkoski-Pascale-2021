from py3d.material.material import Material


class TintEffect(Material):
    """
    Tint colors
    """
    def __init__(self, tint_color=(1, 0, 0)):
        vertex_shader_code = """
        in vec2 vertexPosition;
        in vec2 vertexUV;
        out vec2 UV;
        
        void main()
        {
            gl_Position = vec4(vertexPosition, 0.0, 1.0);
            UV = vertexUV;
        }
        """
        fragment_shader_code = """
        in vec2 UV;
        uniform vec3 tintColor;
        uniform sampler2D textureSampler;
        out vec4 fragColor;
        
        void main()
        {
            vec4 color = texture(textureSampler, UV);
            float gray = (color.r + color.g + color.b) / 3.0;
            fragColor = vec4(gray * tintColor, 1.0);
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("sampler2D", "textureSampler", [None, 1])
        self.add_uniform("vec3", "tintColor", tint_color)
        self.locate_uniforms()
