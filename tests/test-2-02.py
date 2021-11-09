import OpenGL.GL as GL

from opengl_tutorial.core.base import Base
from opengl_tutorial.core.utils import Utils


class Test(Base):
    """ Render a single point """
    def initialize(self):
        print("Initializing program...")
        # initialize program #
        # vertex shader code
        vs_code = """
            void main()
            {
                gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
            }
        """
        # fragment shader code
        fs_code = """
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(1.0, 1.0, 0.0, 1.0);
            }
        """
        # send code to GPU and compile; store program reference
        self._program_ref = Utils.initialize_program(vs_code, fs_code)
        # set up vertex array object #
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        # render settings (optional) #
        # set point width and height
        GL.glPointSize(10)

    def update(self):
        # select program to use when rendering
        GL.glUseProgram(self._program_ref)
        # renders geometric objects using selected program
        GL.glDrawArrays(GL.GL_POINTS, 0, 1)


# instantiate this class and run the program
Test().run()

