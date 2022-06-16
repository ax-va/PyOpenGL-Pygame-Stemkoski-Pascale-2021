from py3d.material.material import Material


class LightedMaterial(Material):
    def __init__(self, number_of_light_sources=1):
        self._number_of_light_sources = number_of_light_sources
        # Create a text line with light uniforms to be inserted into a shader code
        self._light_uniforms = "".join(f"\t\t\tuniform Light light{i};\n"
                                       for i in range(self._number_of_light_sources))
        # Properties vertex_shader_code and fragment_shader_code
        # will be defined in inherited classes FlatMaterial, LambertMaterial,
        # and PhongMaterial
        super().__init__(self.vertex_shader_code, self.fragment_shader_code)
        # Add light uniforms to self._uniform_dict
        for i in range(number_of_light_sources):
            self.add_uniform("Light", f"light{i}", None)

