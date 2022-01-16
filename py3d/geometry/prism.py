from py3d.geometry.cylindrical import CylindricalGeometry


class PrismGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1, sides=6, height_segments=4, closed=True):
        super().__init__(radius, radius, height, sides, height_segments, closed, closed)