import OpenGL.GL as GL

from opengl_tutorial.core.base import Base
from opengl_tutorial.core.utils import Utils
from opengl_tutorial.core.attribute import Attribute


# render two shapes
class Test(Base):
    def initialize(self):
        print("Initializing program...")
        # initialize program #
        vs_code = """
            in vec3 position;
            void main()
            {
                gl_Position = vec4(position.x, position.y, position.z, 1.0);
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
        # render settings #
        GL.glLineWidth(4)
        # set up vertex array object - triangle #
        self._vao_tri = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_tri)
        position_data_tri = [[-0.5,  0.8,  0.0],
                             [-0.2,  0.2,  0.0],
                             [-0.8,  0.2,  0.0]]
        self._vertex_count_tri = len(position_data_tri)
        position_attribute_tri = Attribute('vec3', position_data_tri)
        position_attribute_tri.associate_variable(self._program_ref, 'position')
        # set up vertex array object - square #
        self._vao_square = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_square)
        position_data_square = [[0.8, 0.8, 0.0],
                                [0.8, 0.2, 0.0],
                                [0.2, 0.2, 0.0],
                                [0.2, 0.8, 0.0]]
        self._vertex_count_square = len(position_data_square)
        position_attribute_square = Attribute('vec3', position_data_square)
        position_attribute_square.associate_variable(self._program_ref, 'position')

    def update(self):
        # using same program to render both shapes
        GL.glUseProgram(self._program_ref)
        # draw the triangle
        GL.glBindVertexArray(self._vao_tri)
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, self._vertex_count_tri)
        # draw the square
        GL.glBindVertexArray(self._vao_square)
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, self._vertex_count_square)


# instantiate this class and run the program
Test().run()