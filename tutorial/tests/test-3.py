import OpenGL.GL as GL
from math import pi

from tutorial.core.base import Base
from tutorial.core.utils import Utils
from tutorial.core.attribute import Attribute
from tutorial.core.uniform import Uniform
from tutorial.core.matrix import Matrix


class Test(Base):
    """ Move a triangle around the screen: global and local transformations """
    def initialize(self):
        print('Initializing program...')
        ### initialize program ###
        vs_code = """
            in vec3 position;
            uniform mat4 projectionMatrix;
            uniform mat4 modelMatrix;
            void main()
            {
                gl_Position = projectionMatrix *
                modelMatrix * vec4(position, 1.0);
            }
        """
        fs_code = """
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 1.0, 0.0, 1.0);
            }
        """
        self._program_ref = Utils.initialize_program(vs_code, fs_code)
        ### render settings ###
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        ### set up vertex array object ###
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        ### set up vertex attribute: three points of triangle ###
        position_data = [[0.0,   0.2,  0.0], [0.1,  -0.2,  0.0], [-0.1, -0.2,  0.0]]
        self._vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self._program_ref, 'position')
        ### set up uniforms ###
        m_matrix = Matrix.make_translation(0, 0, -1)
        self._model_matrix = Uniform('mat4', m_matrix)
        self._model_matrix.locate_variable(self._program_ref, 'modelMatrix')
        p_matrix = Matrix.make_perspective()
        self._projection_matrix = Uniform('mat4', p_matrix)
        self._projection_matrix.locate_variable(self._program_ref, 'projectionMatrix')
        # movement speed, units per second
        self._move_speed = 0.5
        # rotation speed, radians per second
        self._turn_speed = 90 * (pi / 180)

    def update(self):
        """ Update data """
        move_amount = self._move_speed * self._delta_time
        turn_amount = self._turn_speed * self._delta_time
        # global translation
        if self._input.is_key_pressed('w'):
            m = Matrix.make_translation(0, move_amount, 0)
            self._model_matrix.data = m @ self._model_matrix.data
        if self._input.is_key_pressed('s'):
            m = Matrix.make_translation(0, -move_amount, 0)
            self._model_matrix.data = m @ self._model_matrix.data
        if self._input.is_key_pressed('a'):
            m = Matrix.make_translation(-move_amount, 0, 0)
            self._model_matrix.data = m @ self._model_matrix.data
        if self._input.is_key_pressed('d'):
            m = Matrix.make_translation(move_amount, 0, 0)
            self._model_matrix.data = m @ self._model_matrix.data
        if self._input.is_key_pressed('z'):
            m = Matrix.make_translation(0, 0, move_amount)
            self._model_matrix.data = m @ self._model_matrix.data
        if self._input.is_key_pressed('x'):
            m = Matrix.make_translation(0, 0, -move_amount)
            self._model_matrix.data = m @ self._model_matrix.data
        # global rotation (around the origin)
        if self._input.is_key_pressed('q'):
            m = Matrix.make_rotation_z(turn_amount)
            self._model_matrix.data = m @ self._model_matrix.data
        if self._input.is_key_pressed('e'):
            m = Matrix.make_rotation_z(-turn_amount)
            self._model_matrix.data = m @ self._model_matrix.data
        # local translation
        if self._input.is_key_pressed('i'):
            m = Matrix.make_translation(0, move_amount, 0)
            self._model_matrix.data = self._model_matrix.data @ m
        if self._input.is_key_pressed('k'):
            m = Matrix.make_translation(0, -move_amount, 0)
            self._model_matrix.data = self._model_matrix.data @ m
        if self._input.is_key_pressed('j'):
            m = Matrix.make_translation(-move_amount, 0, 0)
            self._model_matrix.data = self._model_matrix.data @ m
        if self._input.is_key_pressed('l'):
            m = Matrix.make_translation(move_amount, 0, 0)
            self._model_matrix.data = self._model_matrix.data @ m
        # local rotation (around object center)
        if self._input.is_key_pressed('u'):
            m = Matrix.make_rotation_z(turn_amount)
            self._model_matrix.data = self._model_matrix.data @ m
        if self._input.is_key_pressed('o'):
            m = Matrix.make_rotation_z(-turn_amount)
            self._model_matrix.data = self._model_matrix.data @ m
        ### render scene ###
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glUseProgram(self._program_ref)
        self._projection_matrix.upload_data()
        self._model_matrix.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertex_count)


# instantiate this class and run the program
Test().run()