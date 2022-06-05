from numpy.linalg import inv

from py3d.core.matrix import Matrix
from py3d.core_ext.object3d import Object3D


class Camera(Object3D):
    """  Represents the virtual camera used to view the scene """
    def __init__(self, angle_of_view=60, aspect_ratio=1, near=0.1, far=1000):
        super().__init__()
        self._projection_matrix = Matrix.make_perspective(angle_of_view, aspect_ratio, near, far)
        self._view_matrix = Matrix.make_identity()  # inverse of self._matrix

    @property
    def projection_matrix(self):
        return self._projection_matrix

    @property
    def view_matrix(self):
        return self._view_matrix

    def set_perspective(self, angle_of_view=50, aspect_ratio=1, near=0.1, far=1000):
        self._projection_matrix = Matrix.make_perspective(angle_of_view, aspect_ratio, near, far)

    def set_orthographic(self, left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
        self._projection_matrix = Matrix.make_orthographic(left, right, bottom, top, near, far)

    def update_view_matrix(self):
        self._view_matrix = inv(self.global_matrix)