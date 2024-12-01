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


class Example(Base):
    """ Render two shapes """
    def initialize(self):
        print("Initializing program...")
        # Initialize program #
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
        self.program_ref = Utils.initialize_program(vs_code, fs_code)
        # render settings #
        GL.glLineWidth(4)
        # Set up vertex array object - triangle #
        self.vao_triangle = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_triangle)
        position_data_triangle = [[-0.5,  0.8,  0.0],
                                  [-0.2,  0.2,  0.0],
                                  [-0.8,  0.2,  0.0]]
        self.vertex_count_triangle = len(position_data_triangle)
        position_attribute_triangle = Attribute('vec3', position_data_triangle)
        position_attribute_triangle.associate_variable(self.program_ref, 'position')
        # Set up vertex array object - square #
        self.vao_square = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao_square)
        position_data_square = [[0.8, 0.8, 0.0],
                                [0.8, 0.2, 0.0],
                                [0.2, 0.2, 0.0],
                                [0.2, 0.8, 0.0]]
        self.vertex_count_square = len(position_data_square)
        position_attribute_square = Attribute('vec3', position_data_square)
        position_attribute_square.associate_variable(self.program_ref, 'position')

    def update(self):
        # Using same program to render both shapes
        GL.glUseProgram(self.program_ref)
        # Draw the triangle
        GL.glBindVertexArray(self.vao_triangle)
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, self.vertex_count_triangle)
        # Draw the square
        GL.glBindVertexArray(self.vao_square)
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, self.vertex_count_square)


# Instantiate this class and run the program
Example().run()