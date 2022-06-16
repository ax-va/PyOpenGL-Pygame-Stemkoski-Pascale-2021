import OpenGL.GL as GL

from py3d.material.lighted import LightedMaterial


class LambertMaterial(LightedMaterial):
    """
    Lambert material with at least one light source (or more)
    """
    def __init__(self, texture=None, property_dict={}, number_of_light_sources=1):
        super().__init__(number_of_light_sources)
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        if texture is None:
            self.add_uniform("bool", "useTexture", False)
        else:
            self.add_uniform("bool", "useTexture", True)
            self.add_uniform("sampler2D", "texture", [texture.texture_ref, 1])
        self.locate_uniforms()

        # Render both sides?
        self.setting_dict["doubleSide"] = True
        # Render triangles as wireframe?
        self.setting_dict["wireframe"] = False
        # Set line thickness for wireframe rendering
        self.setting_dict["lineWidth"] = 1

        self.set_properties(property_dict)

    @property
    def vertex_shader_code(self):
        return """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec2 vertexUV;
            in vec3 vertexNormal;
            out vec3 position;
            out vec2 UV;
            out vec3 normal;

            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
                position = vec3(modelMatrix * vec4(vertexPosition, 1));
                UV = vertexUV;
                normal = normalize(mat3(modelMatrix) * vertexNormal);
            }
        """

    @property
    def fragment_shader_code(self):
        return """        
            struct Light
            {
                int lightType;  // 1 = AMBIENT, 2 = DIRECTIONAL, 3 = POINT
                vec3 color;  // used by all lights
                vec3 direction;  // used by directional lights
                vec3 position;  // used by point lights
                vec3 attenuation;  // used by directional lights
            };
        """ + self._light_uniforms + """
            vec3 calculateLight(Light light, vec3 pointPosition, vec3 pointNormal)
            {
                float ambient = 0;
                float diffuse = 0;
                float specular = 0;
                float attenuation = 1;
                vec3 lightDirection = vec3(0, 0, 0);
                
                if (light.lightType == 1)  // ambient light
                {
                    ambient = 1;
                }                
                else if (light.lightType == 2)  // directional light
                {
                    lightDirection = normalize(light.direction);
                }
                else if (light.lightType == 3)  // point light 
                {
                    lightDirection = normalize(pointPosition - light.position);
                    float distance = length(light.position - pointPosition);
                    attenuation = 1.0 / (light.attenuation[0] 
                                       + light.attenuation[1] * distance 
                                       + light.attenuation[2] * distance * distance);
                }
                
                if (light.lightType > 1)  // directional or point light
                {
                    pointNormal = normalize(pointNormal);
                    diffuse = max(dot(pointNormal, -lightDirection), 0.0);
                    diffuse *= attenuation;
                }
                return light.color * (ambient + diffuse + specular);
            }
            
            uniform vec3 baseColor;
            uniform bool useTexture;
            uniform sampler2D texture;
            in vec3 position;
            in vec2 UV;
            in vec3 normal;
            out vec4 fragColor;
            
            void main()
            {
                vec4 color = vec4(baseColor, 1.0);
                if (useTexture)
                    color *= texture2D( texture, UV );
                // Calculate total effect of lights on color
                vec3 total = vec3(0, 0, 0);
                total += calculateLight(light0, position, normal);
                total += calculateLight(light1, position, normal);
                total += calculateLight(light2, position, normal);
                total += calculateLight(light3, position, normal);
                color *= vec4(total, 1);
                fragColor = color;
            }
        """

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