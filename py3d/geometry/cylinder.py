from py3d.geometry.cylindrical import CylindricalGeometry


class CylinderGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1, radial_segments=32, height_segments=1, closed=True):
        super().__init__(radius, radius, height, radial_segments, height_segments, closed, closed)
