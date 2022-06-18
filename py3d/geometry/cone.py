from py3d.geometry.cylindrical import CylindricalGeometry


class ConeGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1, radial_segments=32, height_segments=16, closed=True):
        super().__init__(0, radius, height, radial_segments, height_segments, False, closed)
