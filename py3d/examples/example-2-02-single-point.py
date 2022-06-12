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


class Example(Base):
    """ Render a single point """
    def initialize(self):
        print("Initializing program...")
        # Initialize program #
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
        # Send code to GPU and compile; store program reference
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        # Set up vertex array object #
        vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao_ref)
        # render settings (optional) #
        # Set point width and height
        GL.glPointSize(10)

    def update(self):
        # Select program to use when rendering
        GL.glUseProgram(self.program_ref)
        # Renders geometric objects using selected program
        GL.glDrawArrays(GL.GL_POINTS, 0, 1)


# Instantiate this class and run the program
Example().run()

