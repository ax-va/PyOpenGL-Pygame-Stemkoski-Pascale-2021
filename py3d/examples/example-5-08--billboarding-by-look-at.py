#!/usr/bin/python3
import math
import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from py3d.core.base import Base
from py3d.core.matrix import Matrix
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.core_ext.texture import Texture
from py3d.geometry.box import BoxGeometry
from py3d.geometry.rectangle import RectangleGeometry
from py3d.extras.movement_rig import MovementRig
from py3d.extras.text_texture import TextTexture
from py3d.material.texture import TextureMaterial


class Example(Base):
    """
    Demonstrate billboarding by using look-at.
    A billboard always looks at a moving camera.
    Use keys ADRF to move the camera and see this effect.
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 1, 5])
        self.scene.add(self.rig)

        label_texture = TextTexture(text=" This is a Crate ",
                                    system_font_name="Arial Bold",
                                    font_size=40,
                                    font_color=[0, 0, 200],
                                    image_width=256,
                                    image_height=128,
                                    align_horizontal=0.5,
                                    align_vertical=0.5,
                                    image_border_width=4,
                                    image_border_color=[255, 0, 0])
        label_material = TextureMaterial(label_texture)
        label_geometry = RectangleGeometry(width=1, height=0.5)
        label_geometry.apply_matrix(Matrix.make_rotation_y(math.pi))
        self.label = Mesh(label_geometry, label_material)
        self.label.set_position([0, 1, 0])
        self.scene.add(self.label)

        crate_geometry = BoxGeometry()
        crate_texture = Texture("../images/crate.jpg")
        crate_material = TextureMaterial(crate_texture)
        crate = Mesh(crate_geometry, crate_material)
        self.scene.add(crate)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.label.look_at(self.camera.global_position)
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
