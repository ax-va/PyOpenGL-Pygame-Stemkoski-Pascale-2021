import OpenGL.GL as GL
import numpy as np


class Attribute:
    def __init__(self, data_type, data):
        # type of elements in data array: int | float | vec2 | vec3 | vec4
        self._data_type = data_type
        # array of data to be stored in buffer
        self._data = data
        # reference of available buffer from GPU
        self._buffer_ref = GL.glGenBuffers(1)
        # Upload data immediately
        self.upload_data()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def upload_data(self):
        """ Upload the data to a GPU buffer """
        # Convert data to numpy array format; convert numbers to 32-bit floats
        data = np.array(self._data).astype(np.float32)
        # Select buffer used by the following functions
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._buffer_ref)
        # Store data in currently bound buffer
        GL.glBufferData(GL.GL_ARRAY_BUFFER, data.ravel(), GL.GL_STATIC_DRAW)

    def associate_variable(self, program_ref, variable_name):
        """ Associate variable in program with the buffer """
        # Get reference for program variable with given name
        variable_ref = GL.glGetAttribLocation(program_ref, variable_name)
        # If the program does not reference the variable, then exit
        if variable_ref != -1:
            # Select buffer used by the following functions
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._buffer_ref)
            # Specify how data will be read from the currently bound buffer into the specified variable
            if self._data_type == "int":
                GL.glVertexAttribPointer(variable_ref, 1, GL.GL_INT, False, 0, None)
            elif self._data_type == "float":
                GL.glVertexAttribPointer(variable_ref, 1, GL.GL_FLOAT, False, 0, None)
            elif self._data_type == "vec2":
                GL.glVertexAttribPointer(variable_ref, 2, GL.GL_FLOAT, False, 0, None)
            elif self._data_type == "vec3":
                GL.glVertexAttribPointer(variable_ref, 3, GL.GL_FLOAT, False, 0, None)
            elif self._data_type == "vec4":
                GL.glVertexAttribPointer(variable_ref, 4, GL.GL_FLOAT, False, 0, None)
            else:
                raise Exception(f'Attribute {variable_name} has unknown type {self._data_type}')
            # Indicate that data will be streamed to this variable
            GL.glEnableVertexAttribArray(variable_ref)
