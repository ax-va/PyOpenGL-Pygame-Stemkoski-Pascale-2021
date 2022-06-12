import OpenGL.GL as GL

from py3d.material.material import Material


class PhongMaterial(Material):
    """
    Phong material with four lighting sources
    """
    def __init__(self, texture=None, property_dict={}):
        vertex_shader_code = """
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
        fragment_shader_code = """        
            struct Light
            {
                int lightType;  // 1 = AMBIENT, 2 = DIRECTIONAL, 3 = POINT
                vec3 color;  // used by all lights
                vec3 direction;  // used by point lights
                vec3 position;  // used by point lights
                vec3 attenuation;  // used by point lights
            };
            
            uniform Light light0;
            uniform Light light1;
            uniform Light light2;
            uniform Light light3;
            
            uniform vec3 viewPosition;
            uniform float specularStrength;
            uniform float shininess;

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
                    if (diffuse > 0)
                    {
                        vec3 viewDirection = normalize(viewPosition - pointPosition);
                        vec3 reflectDirection = reflect(lightDirection, pointNormal);
                        specular = max(dot(viewDirection, reflectDirection), 0.0);
                        specular = specularStrength * pow(specular, shininess);
                    }
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
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform("Light", "light0", None)
        self.add_uniform("Light", "light1", None)
        self.add_uniform("Light", "light2", None)
        self.add_uniform("Light", "light3", None)
        if texture is None:
            self.add_uniform("bool", "useTexture", False)
        else:
            self.add_uniform("bool", "useTexture", True)
            self.add_uniform("sampler2D", "texture", [texture.texture_ref, 1])
        self.add_uniform("vec3", "viewPosition", [0, 0, 0])
        self.add_uniform("float", "specularStrength", 1.0)
        self.add_uniform("float", "shininess", 32.0)
        self.locate_uniforms()

        # Render both sides?
        self.setting_dict["doubleSide"] = True
        # Render triangles as wireframe?
        self.setting_dict["wireframe"] = False
        # Set line thickness for wireframe rendering
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
