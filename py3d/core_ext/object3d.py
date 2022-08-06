import numpy as np
from py3d.core.matrix import Matrix


class Object3D:
    """ Represent a node in the scene graph tree structure """
    def __init__(self):
        # local transform matrix with respect to the parent of the object
        self._matrix = Matrix.make_identity()
        self._parent = None
        self._children_list = []

    @property
    def children_list(self):
        return self._children_list

    @children_list.setter
    def children_list(self, children_list):
        self._children_list = children_list

    @property
    def descendant_list(self):
        """ Return a single list containing all descendants """
        # master list of all descendant nodes
        descendant_list = []
        # nodes to be added to descendant list,
        # and whose children will be added to this list
        nodes_to_process = [self]
        # continue processing nodes while any are left
        while len(nodes_to_process) > 0:
            # remove first node from list
            node = nodes_to_process.pop(0)
            # add this node to descendant list
            descendant_list.append(node)
            # children of this node must also be processed
            nodes_to_process = node._children_list + nodes_to_process
        return descendant_list

    @property
    def global_matrix(self):
        """
        Calculate the transformation of this Object3D
        relative to the root Object3D of the scene graph
        """
        if self._parent is None:
            return self._matrix
        else:
            return self._parent.global_matrix @ self._matrix

    @property
    def global_position(self):
        """ Return the global or world position of the object """
        return [self.global_matrix.item((0, 3)),
                self.global_matrix.item((1, 3)),
                self.global_matrix.item((2, 3))]

    @property
    def local_matrix(self):
        return self._matrix

    @local_matrix.setter
    def local_matrix(self, matrix):
        self._matrix = matrix

    @property
    def local_position(self):
        """
        Return the local position of the object (with respect to its parent)
        """
        # The position of an object can be determined from entries in the
        # last column of the transform matrix
        return [self._matrix.item((0, 3)),
                self._matrix.item((1, 3)),
                self._matrix.item((2, 3))]

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def rotation_matrix(self):
        """
        Returns 3x3 submatrix with rotation data.
        3x3 top-left submatrix contains only rotation data.
        """
        return np.array(
            [self._matrix[0][0:3],
             self._matrix[1][0:3],
             self._matrix[2][0:3]]
        ).astype(float)

    @property
    def direction(self):
        forward = np.array([0, 0, -1]).astype(float)
        return list(self.rotation_matrix @ forward)

    def add(self, child):
        self._children_list.append(child)
        child.parent = self

    def remove(self, child):
        self._children_list.remove(child)
        child.parent = None

    # apply geometric transformations
    def apply_matrix(self, matrix, local=True):
        if local:
            # local transform
            self._matrix = self._matrix @ matrix
        else:
            # global transform
            self._matrix = matrix @ self._matrix

    def translate(self, x, y, z, local=True):
        m = Matrix.make_translation(x, y, z)
        self.apply_matrix(m, local)

    def rotate_x(self, angle, local=True):
        m = Matrix.make_rotation_x(angle)
        self.apply_matrix(m, local)

    def rotate_y(self, angle, local=True):
        m = Matrix.make_rotation_y(angle)
        self.apply_matrix(m, local)

    def rotate_z(self, angle, local=True):
        m = Matrix.make_rotation_z(angle)
        self.apply_matrix(m, local)

    def scale(self, s, local=True):
        m = Matrix.make_scale(s)
        self.apply_matrix(m, local)

    def set_position(self, position):
        """ Set the local position of the object """
        self._matrix.itemset((0, 3), position[0])
        self._matrix.itemset((1, 3), position[1])
        self._matrix.itemset((2, 3), position[2])

    def look_at(self, target_position):
        self._matrix = Matrix.make_look_at(self.global_position, target_position)

    def set_direction(self, direction):
        position = self.local_position
        target_position = [
            position[0] + direction[0],
            position[1] + direction[1],
            position[2] + direction[2]
        ]
        self.look_at(target_position)

