from py3d.geometry.parametric import ParametricGeometry


class PlaneGeometry(ParametricGeometry):
    def __init__(self, width=1, height=1, width_segments=8, height_segments=8):
        super().__init__(-width / 2, width / 2, width_segments,
                         -height / 2, height / 2, height_segments,
                         lambda u, v: [u, v, 0])
