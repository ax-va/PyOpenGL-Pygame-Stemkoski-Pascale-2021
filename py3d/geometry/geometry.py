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
    def attributes(self):
        return self._attributes

    def add_attribute(self, data_type, variable_name, data):
        self._attribute_dict[variable_name] = Attribute(data_type, data)

    def count_vertices(self):
        # Number of vertices may be calculated from the length of
        # any Attribute object's array of data
        attribute = list(self._attribute_dict.values())[0]
        self._vertex_count = len(attribute.data)