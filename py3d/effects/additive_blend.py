from py3d.material.material import Material


class AdditiveBlendEffect(Material):
    def __init__(self, blend_texture, original_strength=1, blend_strength=1):
        #  pass-through shader
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
        #  pass-through shader
        fragment_shader_code = """
        in vec2 UV;
        uniform sampler2D textureSampler;
        uniform sampler2D blendTextureSampler;
        uniform float originalStrength;
        uniform float blendStrength;
        out vec4 fragColor;

        void main()
        {
            vec4 originalColor = texture(textureSampler, UV);
            vec4 blendColor = texture(blendTextureSampler, UV);
            vec4 color = originalStrength * originalColor + blendStrength * blendColor;
            fragColor = color;
        }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("sampler2D", "textureSampler", [None, 1])
        self.add_uniform("sampler2D", "blendTextureSampler", [blend_texture.texture_ref, 2])
        self.add_uniform("float", "originalStrength", original_strength)
        self.add_uniform("float", "blendStrength", blend_strength)
        self.locate_uniforms()
