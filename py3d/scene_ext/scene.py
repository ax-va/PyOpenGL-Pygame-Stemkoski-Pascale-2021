from py3d.scene_ext.object_3d import Object3D

class Scene(Object3D):
    """  Represents the root node of the tree """

    def __init__(self):
        super().__init__()