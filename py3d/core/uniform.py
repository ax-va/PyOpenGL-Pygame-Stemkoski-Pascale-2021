import OpenGL.GL as GL


class Uniform:
    def __init__(self, data_type, data):
        # type of data:
        # int | bool | float | vec2 | vec3 | vec4
        self._data_type = data_type
        # data to be sent to uniform variable
        self._data = data
        # reference for variable location in program
        self._variable_ref = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def locate_variable(self, program_ref, variable_name):
        """ Get and store reference for program variable with given name """
        self._variable_ref = GL.glGetUniformLocation(program_ref, variable_name)

    def upload_data(self):
        """ Store data in uniform variable previously located """
        # If the program does not reference the variable, then exit
        if self._variable_ref != -1:
            if self._data_type == 'int':
                GL.glUniform1i(self._variable_ref, self._data)
            elif self._data_type == 'bool':
                GL.glUniform1i(self._variable_ref, self._data)
            elif self._data_type == 'float':
                GL.glUniform1f(self._variable_ref, self._data)
            elif self._data_type == 'vec2':
                GL.glUniform2f(self._variable_ref, self._data[0], self._data[1])
            elif self._data_type == 'vec3':
                GL.glUniform3f(self._variable_ref, self._data[0], self._data[1], self._data[2])
            elif self._data_type == 'vec4':
                GL.glUniform4f(self._variable_ref, self._data[0], self._data[1], self._data[2], self._data[3])
            elif self._data_type == 'mat4':
                GL.glUniformMatrix4fv(self._variable_ref, 1, GL.GL_TRUE, self._data)
