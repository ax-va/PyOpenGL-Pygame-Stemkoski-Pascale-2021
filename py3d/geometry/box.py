from py3d.geometry.geometry import Geometry


class BoxGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1):
        super().__init__()
        # vertices
        p0 = [-width / 2, -height / 2, -depth / 2]
        p1 = [width / 2, -height / 2, -depth / 2]
        p2 = [-width / 2, height / 2, -depth / 2]
        p3 = [width / 2, height / 2, -depth / 2]
        p4 = [-width / 2, -height / 2, depth / 2]
        p5 = [width / 2, -height / 2, depth / 2]
        p6 = [-width / 2, height / 2, depth / 2]
        p7 = [width / 2, height / 2, depth / 2]
        # colors for faces in order:
        # x+, x-, y+, y-, z+, z-
        c1, c2 = [1, 0.5, 0.5], [0.5, 0, 0]
        c3, c4 = [0.5, 1, 0.5], [0, 0.5, 0]
        c5, c6 = [0.5, 0.5, 1], [0, 0, 0.5]
        # texture coordinates
        t0, t1, t2, t3 = [0, 0], [1, 0], [0, 1], [1, 1]
        # Each side consists of two triangles
        position_data = [p5, p1, p3, p5, p3, p7,
                         p0, p4, p6, p0, p6, p2,
                         p6, p7, p3, p6, p3, p2,
                         p0, p1, p5, p0, p5, p4,
                         p4, p5, p7, p4, p7, p6,
                         p1, p0, p2, p1, p2, p3]
        color_data = [c1] * 6 + [c2] * 6 + [c3] * 6 \
                   + [c4] * 6 + [c5] * 6 + [c6] * 6
        uv_data = [t0, t1, t3, t0, t3, t2] * 6
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        # normal vectors for x+, x-, y+, y-, z+, z-
        n1, n2 = [1, 0, 0], [-1, 0, 0]
        n3, n4 = [0, 1, 0], [0, -1, 0]
        n5, n6 = [0, 0, 1], [0, 0, -1]
        normal_data = [n1]*6 + [n2]*6 + [n3]*6 + [n4]*6 + [n5]*6 + [n6]*6
        self.add_attribute("vec3", "vertexNormal", normal_data)
        self.add_attribute("vec3", "faceNormal", normal_data)
