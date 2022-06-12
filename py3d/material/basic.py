from py3d.material.material import Material
from py3d.core.uniform import Uniform


class BasicMaterial(Material):
    def __init__(self, vertex_shader_code=None, fragment_shader_code=None, use_vertex_colors=True):
        if vertex_shader_code is None:
            vertex_shader_code = """
                uniform mat4 projectionMatrix;
                uniform mat4 viewMatrix;
                uniform mat4 modelMatrix;
                in vec3 vertexPosition;
                in vec3 vertexColor;
                out vec3 color;    
                        
                void main()
                {
                    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                    color = vertexColor;
                }
            """
        if fragment_shader_code is None:
            fragment_shader_code = """
                uniform vec3 baseColor;
                uniform bool useVertexColors;
                in vec3 color;
                out vec4 fragColor;
                
                void main()
                {
                    fragColor = vec4(baseColor, 1.0);
                    if (useVertexColors) 
                    {
                        fragColor = vec4(color, 1.0);
                    }
                }
            """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        if use_vertex_colors:
            self.add_uniform("bool", "useVertexColors", False)
        self.locate_uniforms()
