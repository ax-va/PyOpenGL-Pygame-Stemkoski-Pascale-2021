from py3d.material.material import Material


class DepthMaterial(Material):

    def __init__(self):
        # vertex shader code
        vertex_shader_code = """
        in vec3 vertexPosition;
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        
        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }
        """

        # fragment shader code
        fragment_shader_code = """
        out vec4 fragColor;
        
        void main()
        {
            float z = gl_FragCoord.z;
            fragColor = vec4(z, z, z, 1);
        }
        """
        
        # Initialize shaders
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.locate_uniforms()
