from py3d.core_ext.object3d import Object3D


class Group(Object3D):
    """
    Represents an interior node to which other nodes are attached
    to more easily transform them as a single unit
    """
    def __init__(self):
        super().__init__()