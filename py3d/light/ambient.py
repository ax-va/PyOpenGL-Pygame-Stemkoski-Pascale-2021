from py3d.light.light import Light


class AmbientLight(Light):
    def __init__(self, color=(1, 1, 1)):
        super().__init__(Light.AMBIENT)
        self._color = color
