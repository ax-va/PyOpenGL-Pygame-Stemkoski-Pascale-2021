from py3d.material.material import Material


class PixelateEffect(Material):
    """
    Pixelation
    """
    def __init__(self, pixel_size=8, resolution=(512, 512)):
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
        uniform float pixelSize;
        uniform vec2 resolution;
        out vec4 fragColor;

        void main()
        {
            vec2 factor = resolution / pixelSize;
            vec2 newUV = floor(UV * factor) / factor;
            vec4 color = texture(textureSampler, newUV);
            fragColor = color;
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("sampler2D", "textureSampler", [None, 1])
        self.add_uniform("float", "pixelSize", pixel_size)
        self.add_uniform("vec2", "resolution", resolution)
        self.locate_uniforms()
