from py3d.extras.grid import GridHelper


class DirectionalLightHelper(GridHelper):
    def __init__(self, directional_light):
        color = directional_light.color
        super().__init__(
            size=1,
            divisions=6,
            grid_color=color,
            center_color=color
        )
        self.geometry.attribute_dict["vertexPosition"].data.extend([[0, 0, 0], [0, 0, -10]])
        self.geometry.attribute_dict["vertexColor"].data.extend([color, color])
        self.geometry.upload_data(["vertexPosition", "vertexColor"])
