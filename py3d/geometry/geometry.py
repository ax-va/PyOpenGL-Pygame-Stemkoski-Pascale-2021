import numpy as np
from py3d.core.attribute import Attribute


class Geometry:
    """ Stores attribute data and the total number of vertices """
    def __init__(self):
        # Store Attribute objects, indexed by name of associated variable in shader.
        # Shader variable associations set up later and stored in vertex array object in Mesh.
        self._attribute_dict = {}
        # number of vertices
        self._vertex_count = None

    @property
    def attribute_dict(self):
        return self._attribute_dict

    @property
    def vertex_count(self):
        return self._vertex_count

    def add_attribute(self, data_type, variable_name, data):
        attribute = Attribute(data_type, data)
        self._attribute_dict[variable_name] = attribute
        # Update the vertex count
        if variable_name == "vertexPosition":
            # Number of vertices may be calculated from
            # the length of any Attribute object's array of data
            self._vertex_count = len(data)

    def upload_data(self, variable_names=None):
        if not variable_names:
            variable_names = self._attribute_dict.keys()
        for variable_name in variable_names:
            self._attribute_dict[variable_name].upload_data()
            # Update the vertex count
            if variable_name == "vertexPosition":
                # Number of vertices may be calculated from
                # the length of any Attribute object's array of data
                self._vertex_count = len(self._attribute_dict[variable_name].data)

    def apply_matrix(self, matrix):
        """ Transform the data in an attribute using a matrix """
        old_position_data = self._attribute_dict["vertexPosition"].data
        new_position_data = []
        for old_pos in old_position_data:
            # Avoid changing list references
            new_pos = old_pos.copy()
            # Add the homogeneous fourth coordinate
            new_pos.append(1)
            # Multiply by matrix.
            # No need to transform new_pos to np.array.
            new_pos = matrix @ new_pos
            # Remove the homogeneous coordinate
            new_pos = list(new_pos[0:3])
            # Add to the new data list
            new_position_data.append(new_pos)
        self._attribute_dict["vertexPosition"].data = new_position_data
        # New data must be uploaded
        self._attribute_dict["vertexPosition"].upload_data()
        self._vertex_count = len(new_position_data)

        # Extract the rotation submatrix
        rotation_matrix = np.array(
            [matrix[0][0:3],
             matrix[1][0:3],
             matrix[2][0:3]]
        ).astype(float)

        old_vertex_normal_data = self._attribute_dict["vertexNormal"].data
        new_vertex_normal_data = []
        for old_normal in old_vertex_normal_data:
            # Avoid changing list references
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_vertex_normal_data.append(new_normal)
        self._attribute_dict["vertexNormal"].data = new_vertex_normal_data
        # New data must be uploaded
        self._attribute_dict["vertexNormal"].upload_data()

        old_face_normal_data = self._attribute_dict["faceNormal"].data
        new_face_normal_data = []
        for old_normal in old_face_normal_data:
            # Avoid changing list references
            new_normal = old_normal.copy()
            new_normal = rotation_matrix @ new_normal
            new_face_normal_data.append(new_normal)
        self._attribute_dict["faceNormal"].data = new_face_normal_data
        # New data must be uploaded
        self._attribute_dict["faceNormal"].upload_data()

    def merge(self, other_geometry):
        """
        Merge data from attributes of other geometry into this object.
        Requires both geometries to have attributes with same names.
        """
        for variable_name, attribute_instance in self._attribute_dict.items():
            attribute_instance.data.extend(other_geometry.attribute_dict[variable_name].data)
            # New data must be uploaded
            attribute_instance.upload_data()

