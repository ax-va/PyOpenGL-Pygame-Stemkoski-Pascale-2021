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
from py3d.geometry.rectangle import RectangleGeometry
from py3d.extras.text_texture import TextTexture
from py3d.material.texture import TextureMaterial


class Example(Base):
    """ Render a rotating rectangle with a text texture """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 1.5])
        geometry = RectangleGeometry()
        message = TextTexture(text="Python Graphics",
                              system_font_name="Impact",
                              font_size=32,
                              font_color=[0, 0, 200],
                              image_width=256,
                              image_height=256,
                              align_horizontal=0.5,
                              align_vertical=0.5,
                              image_border_width=4,
                              image_border_color=[255, 0, 0])
        material = TextureMaterial(message)
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.mesh.rotate_y(0.0114)
        self.mesh.rotate_x(0.0237)
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
