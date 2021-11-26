import OpenGL.GL as GL
import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from pyopengl_pygame.core.base import Base
from pyopengl_pygame.core.utils import Utils
from pyopengl_pygame.core.attribute import Attribute
from pyopengl_pygame.core.uniform import Uniform


class Example(Base):
    """ Enables the user to move a triangle using the arrow keys """
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
        # render settings (optional) #
        # specify color used when clearly
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
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
        self._translation = Uniform('vec3', [-0.5, 0.0, 0.0])
        self._translation.locate_variable(self._program_ref, 'translation')
        self._base_color = Uniform('vec3', [1.0, 0.0, 0.0])
        self._base_color.locate_variable(self._program_ref, 'baseColor')
        # triangle speed, units per second
        self._speed = 0.5

    def update(self):
        """ Update data """
        distance = self._speed * self._delta_time
        if self._input.is_key_pressed('left'):
            self._translation.data[0] -= distance
        if self._input.is_key_pressed('right'):
            self._translation.data[0] += distance
        if self._input.is_key_pressed('down'):
            self._translation.data[1] -= distance
        if self._input.is_key_pressed('up'):
            self._translation.data[1] += distance
        # reset color buffer with specified color
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self._program_ref)
        self._translation.upload_data()
        self._base_color.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertex_count)


# instantiate this class and run the program
Example().run()
