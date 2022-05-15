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
        self._attribute_dict[variable_name] = Attribute(data_type, data)

    def apply_matrix(self, matrix, variable_name="vertexPosition"):
        """ Transform the data in an attribute using a matrix """
        old_position_data = self._attribute_dict[variable_name].data
        new_position_data = []
        for old_pos in old_position_data:
            # Avoid changing list references
            new_pos = old_pos.copy()
            # Add the homogeneous fourth coordinate
            new_pos.append(1)
            # Multiply by matrix
            new_pos = matrix @ new_pos
            # Remove the homogeneous coordinate
            new_pos = list(new_pos[0:3])
            # Add to the new data list
            new_position_data.append(new_pos)
        self._attribute_dict[variable_name].data = new_position_data
        # New data must be uploaded
        self._attribute_dict[variable_name].upload_data()

    def count_vertices(self):
        # Number of vertices may be calculated from the length of
        # any Attribute object's array of data
        attribute = list(self._attribute_dict.values())[0]
        self._vertex_count = len(attribute.data)

    def merge(self, other_geometry):
        """
        Merge data from attributes of other geometry into this object.
        Requires both geometries to have attributes with same names.
        """
        for variable_name, attribute_object in self._attribute_dict.items():
            attribute_object.data += other_geometry._attribute_dict[variable_name].data
            # New data must be uploaded
            attribute_object.upload_data()
