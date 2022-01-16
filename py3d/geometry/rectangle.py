from py3d.geometry.geometry import Geometry


class RectangleGeometry(Geometry):
    def __init__(self, width=1, height=1):
        super().__init__()
        # vertices
        p0 = [-width/2, -height/2, 0]
        p1 = [ width/2, -height/2, 0]
        p2 = [-width/2,  height/2, 0]
        p3 = [ width/2,  height/2, 0]
        # colors
        c0, c1, c2, c3 = [1, 1,1 ], [1, 0, 0], [0, 1, 0], [0, 0, 1]
        # triangles p0-p1-p3 and p0-p3-p2
        position_data = [p0, p1, p3, p0, p3, p2]
        color_data = [c0, c1, c3, c0, c3, c2]
        # color_data = [c0, c0, c0, c1, c1, c1]
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec3", "vertexColor", color_data)
        self.count_vertices()