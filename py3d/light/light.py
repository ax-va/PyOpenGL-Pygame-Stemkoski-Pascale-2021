from py3d.core_ext.object3d import Object3D


class Light(Object3D):
    AMBIENT = 1
    DIRECTIONAL = 2
    POINT = 3

    def __init__(self, light_type=0):
        super().__init__()
        self._light_type = light_type
        self._color = [1, 1, 1]
        self._attenuation = [1, 0, 0]

    @property
    def light_type(self):
        return self._light_type

    @property
    def color(self):
        return self._color

    @property
    def attenuation(self):
        return self._attenuation
