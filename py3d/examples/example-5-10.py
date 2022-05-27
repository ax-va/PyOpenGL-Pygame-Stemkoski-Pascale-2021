import math
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
from py3d.core_ext.texture import Texture
from py3d.geometry.box import BoxGeometry
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.texture import TextureMaterial
from py3d.extras.movement_rig import MovementRig
from py3d.extras.grid import GridHelper
from py3d.extras.text_texture import TextTexture


class Example(Base):
    """
    Demonstrate a heads-up display (HUD): a transparent layer containing some images
    (for example, with a text), rendered afer the main scene, and appearing on the top layer.
    Move the camera: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 0.5, 3])
        self.scene.add(self.rig)

        crate_geometry = BoxGeometry()
        crate_material = TextureMaterial(Texture("../images/crate.jpg"))
        crate = Mesh(crate_geometry, crate_material)
        crate.translate(0, 0.5, 0)
        self.scene.add(crate)

        grid = GridHelper(grid_color=[1, 1, 1], center_color=[1, 1, 0])
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

        self.hud_scene = Scene()
        self.hud_camera = Camera()
        self.hud_camera.set_orthographic(0, 800, 0, 600, 1, -1)

        label_geo1 = RectangleGeometry(
            width=400, height=200,
            position=[0, 600],
            alignment=[0, 1]
        )
        label_mat1 = TextureMaterial(Texture("../images/crate-simulator.png"))
        label1 = Mesh(label_geo1, label_mat1)
        self.hud_scene.add(label1)

        label_geo2 = RectangleGeometry(
            width=200, height=200,
            position=[800, 0],
            alignment=[1, 0]
        )
        message = TextTexture(
            text="Version 1.0",
            system_font_name="Ink Free",
            font_size=32,
            font_color=[127, 255, 127],
            image_width=200,
            image_height=200,
            transparent=True
        )
        label_mat2 = TextureMaterial(message)
        label2 = Mesh(label_geo2, label_mat2)
        self.hud_scene.add(label2)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)
        self.renderer.render(
            scene=self.hud_scene,
            camera=self.hud_camera,
            clear_color=False
        )


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
