from py3d.geometry.geometry import EllipsoidGeometry


class SphereGeometry(EllipsoidGeometry):
    def __init__(self, radius=1, radius_segments=32, height_segments=16):
        super().__init__(2*radius, 2*radius, 2*radius, radius_segments, height_segments)