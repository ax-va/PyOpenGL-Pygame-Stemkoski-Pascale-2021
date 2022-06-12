#!/usr/bin/python3
import OpenGL.GL as GL
import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from py3d.core.base import Base
from py3d.core.utils import Utils
from py3d.core.attribute import Attribute
from py3d.core.uniform import Uniform


class Example(Base):
    """ Render two triangles with different positions and colors """
    def initialize(self):
        print("Initializing program...")
        # Initialize program #
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
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        # Set up vertex array object #
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        # Set up vertex attribute #
        position_data = [[ 0.0,  0.2,  0.0],
                         [ 0.2, -0.2,  0.0],
                         [-0.2, -0.2,  0.0]]
        self.vertex_count = len(position_data)
        position_attribute = Attribute('vec3', position_data)
        position_attribute.associate_variable(self.program_ref, 'position')
        # Set up uniforms #
        self.translation1 = Uniform('vec3', [-0.5, 0.0, 0.0])
        self.translation1.locate_variable(self.program_ref, 'translation')
        self.translation2 = Uniform('vec3', [0.5, 0.0, 0.0])
        self.translation2.locate_variable(self.program_ref, 'translation')
        self.base_color1 = Uniform('vec3', [1.0, 0.0, 0.0])
        self.base_color1.locate_variable(self.program_ref, 'baseColor')
        self.base_color2 = Uniform('vec3', [0.0, 0.0, 1.0])
        self.base_color2.locate_variable(self.program_ref, 'baseColor')

    def update(self):
        GL.glUseProgram(self.program_ref)
        # Draw the first triangle
        self.translation1.upload_data()
        self.base_color1.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)
        # Draw the second triangle
        self.translation2.upload_data()
        self.base_color2.upload_data()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)


# Instantiate this class and run the program
Example().run()
