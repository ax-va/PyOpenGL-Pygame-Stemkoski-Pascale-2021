from py3d.material.material import Material


class InvertEffect(Material):
    """
    Invert colors
    """
    def __init__(self):
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
        uniform sampler2D textureSampler;
        out vec4 fragColor;
        
        void main()
        {
            vec4 color = texture(textureSampler, UV);
            vec4 invert = vec4(1 - color.r, 1 - color.g, 1 - color.b, 1);
            fragColor = invert;
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("sampler2D", "textureSampler", [None, 1])
        self.locate_uniforms()
