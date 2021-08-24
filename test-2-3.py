import OpenGL.GL as GL

from opengl_tutorial.core.base import Base
from opengl_tutorial.core.utils import Utils
from opengl_tutorial.core.attribute import Attribute


# render six points in a hexagon arrangement
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
        # render settings (optional) #
        GL.glLineWidth(4)
        # set up vertex array object #
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        # set up vertex attribute #
        position_data = [[ 0.8,  0.0,  0.0],
                         [ 0.4,  0.6,  0.0],
                         [-0.4,  0.6,  0.0],
                         [-0.8,  0.0,  0.0],
                         [-0.4, -0.6,  0.0],
                         [ 0.4, -0.6,  0.0]]
        self._vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self._program_ref, 'position')

    def update(self):
        GL.glUseProgram(self._program_ref)
        # GL.glDrawArrays(GL.GL_LINE_LOOP, 0 , self._vertex_count)
        # GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertex_count)
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, self._vertex_count)


# instantiate this class and run the program
Test().run()