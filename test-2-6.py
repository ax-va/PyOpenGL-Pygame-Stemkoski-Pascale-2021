import OpenGL.GL as GL

from opengl_tutorial.core.base import Base
from opengl_tutorial.core.utils import Utils
from opengl_tutorial.core.attribute import Attribute
from opengl_tutorial.core.uniform import Uniform


class Test(Base):
    """ Render two triangles with different positions and colors """

    def initialize(self):
        print("Initializing program...")
        # initialize program #
        vs_code = """
            in vec3 position;
            uniform vec3 translation;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
            }
        """
        fs_code = """
            uniform vec3 baseColor;
            out vec4 fragColor;
            void main()
            {
                fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
            }
        """
        self._program_ref = Utils.initialize_program(vs_code, fs_code)
        # set up vertex array object #
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        # set up vertex attribute #
        position_data = [[ 0.0,  0.2,  0.0],
                         [ 0.2, -0.2,  0.0],
                         [-0.2, -0.2,  0.0]]
        self._vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self._program_ref, 'position')
        # set up uniforms #
        self._translation1 = Uniform('vec3', [-0.5, 0.0, 0.0])
        self._translation1.locate_variable(self._program_ref, 'translation')
        self._translation2 = Uniform('vec3', [0.5, 0.0, 0.0])
        self._translation2.locate_variable(self._program_ref, 'translation')
        self._base_color1 = Uniform('vec3', [1.0, 0.0, 0.0])
        self._base_color1.locate_variable(self._program_ref, 'baseColor')
        self._base_color2 = Uniform('vec3', [0.0, 0.0, 1.0])
        self._base_color2.locate_variable(self._program_ref, 'baseColor')

    def update(self):
        GL.glUseProgram(self._program_ref)
        # draw the first triangle
        self._translation1.upload_data()
        self._base_color1.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertex_count)
        # draw the second triangle
        self._translation2.upload_data()
        self._base_color2.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertex_count)


# instantiate this class and run the program
Test().run()
