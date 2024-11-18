#!/usr/bin/python3
import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.geometry.sphere import SphereGeometry
from py3d.material.material import Material


class Example(Base):
    """ Render a spinning sphere with gradient colors """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 7])
        geometry = SphereGeometry(radius=3)
        vs_code = """
        uniform mat4 modelMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 projectionMatrix;
        in vec3 vertexPosition;
        out vec3 position;
        void main()
        {
            vec4 pos = vec4(vertexPosition, 1.0);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
            position = vertexPosition;
        }
        """
        fs_code = """
        in vec3 position;
        out vec4 fragColor;
        void main()
        {
            vec3 color = mod(position, 1.0);
            fragColor = vec4(color, 1.0);
        }
        """
        material = Material(vs_code, fs_code)
        material.locate_uniforms()
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.mesh.rotate_y(0.00514)
        self.mesh.rotate_x(0.00337)
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()