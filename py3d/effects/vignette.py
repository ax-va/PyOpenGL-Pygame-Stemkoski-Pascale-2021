from py3d.material.material import Material


class VignetteEffect(Material):
    """
    Vignette Effect
    """
    def __init__(self,
                 dimming_start=0.4,
                 dimming_end=1.0,
                 dimming_color=(0, 0, 0)):
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
        uniform float dimStart;
        uniform float dimEnd;
        uniform vec3 dimColor;
        out vec4 fragColor;

        void main()
        {
            vec4 color = texture(textureSampler, UV);
            // Calculate position in clip space from UV coordinates
            vec2 position = 2 * UV - vec2(1, 1);
            // Calculate distance from center, which affects brightness
            float d = length(position);
            // Calculate brightness factor
            // if d = dimStart, then b = 1; if d = dimEnd, then b = 0
            float b = (d - dimEnd) / (dimStart - dimEnd);
            // Prevent oversaturation
            b = clamp(b, 0, 1);
            // Mix the texture color and dim color 
            fragColor = vec4(b * color.rgb + (1 - b) * dimColor, 1);
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("sampler2D", "textureSampler", [None, 1])
        self.add_uniform("float", "dimStart", dimming_start)
        self.add_uniform("float", "dimEnd", dimming_end)
        self.add_uniform("vec3", "dimColor", dimming_color)
        self.locate_uniforms()
