from py3d.material.material import Material


class LightedMaterial(Material):
    def __init__(self, number_of_light_sources=1):
        self._number_of_light_sources = number_of_light_sources
        # Properties vertex_shader_code and fragment_shader_code
        # will be defined in inherited classes FlatMaterial, LambertMaterial,
        # and PhongMaterial
        super().__init__(self.vertex_shader_code, self.fragment_shader_code)
        # Add light uniforms to self._uniform_dict
        for i in range(self._number_of_light_sources):
            self.add_uniform("Light", f"light{i}", None)

    @property
    def declaring_light_uniforms_in_shader_code(self):
        """ Create a text line with light uniforms to be inserted into a shader code """
        return "\n" + "\n".join(f"\t\t\tuniform Light light{i};"
                                for i in range(self._number_of_light_sources)) + "\n"

    @property
    def adding_lights_in_shader_code(self):
        return "\n" + "\n".join(f"\t\t\t\tlight += calculateLight(light{i}, position, calcNormal);"
                                for i in range(self._number_of_light_sources))

    @property
    def vertex_shader_code(self):
        raise NotImplementedError("Implement this property for an inheriting class")

    @property
    def fragment_shader_code(self):
        raise NotImplementedError("Implement this property for an inheriting class")
