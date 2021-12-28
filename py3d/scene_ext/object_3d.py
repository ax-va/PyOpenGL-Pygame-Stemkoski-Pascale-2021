from py3d.core.matrix import Matrix


class Object3D:
    """  Represent a node in the scene graph tree structure  """
    def __init__(self):
        # Local transform matrix with respect to the parent of the object
        self._transform = Matrix.make_identity()
        self._parent = None
        self._children = []

    @property
    def descendant_list(self):
        """  Return a single list containing all descendants  """
        # master list of all descendant nodes
        descendants = []
        # nodes to be added to descendant list,
        # and whose children will be added to this list
        nodes_to_process = [self]
        # continue processing nodes while any are left
        while len(nodes_to_process) > 0:
            # remove first node from list
            node = nodes_to_process.pop(0)
            # add this node to descendant list
            descendants.append(node)
            # children of this node must also be processed
            nodes_to_process = node.children + nodes_to_process
        return descendants

    @property
    def global_matrix(self):
        """  Calculate a transformation of this Object3D relative
             to the root Object3D of the scene graph  """
        if self._parent is None:
            return self._transform
        else:
            return self._parent.global_matrix @ self._transform

    @property
    def local_matrix(self):
        return self._transform

    def add(self, child):
        self._children.append(child)
        child.parent = self

    def remove(self, child):
        self._children.remove(child)
        child.parent = None

    # apply geometric transformations
    def apply_matrix(self, matrix, local=True):
        if local:
            self._transform = self._transform @ matrix
        else:
            self._transform = matrix @ self._transform

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

    def get_position(self):
        """   Return the local position of the object (with respect to its parent)  """
        # The position of an object can be determined from entries in the
        # last column of the transform matrix
        return [self._transform.item((0, 3)),
                self._transform.item((1, 3)),
                self._transform.item((2, 3))]

    def get_world_position(self):
        """   Return the global or world position of the object  """
        world_transform = self.get_world_matrix()
        return [world_transform.item((0, 3)),
                world_transform.item((1, 3)),
                world_transform.item((2, 3))]

    def set_position(self, position):
        """   Set the local position of the object  """
        self._transform.itemset((0, 3), position[0])
        self._transform.itemset((1, 3), position[1])
        self._transform.itemset((2, 3), position[2])
