from py3d.material.material import Material


class ColorReduceEffect(Material):
    """
    Reduce colors
    """
    def __init__(self, levels=5):
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
        uniform float levels;
        out vec4 fragColor;

        void main()
        {
            vec4 color = texture(textureSampler, UV);
            vec4 reduced = round(color * levels) / levels;
            reduced.a = 1.0;
            fragColor = reduced;
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("sampler2D", "textureSampler", [None, 1])
        self.add_uniform("float", "levels", levels)
        self.locate_uniforms()
