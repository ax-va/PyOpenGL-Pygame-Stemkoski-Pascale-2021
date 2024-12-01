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
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.geometry.box import BoxGeometry
from py3d.extras.axes import AxesHelper
from py3d.extras.grid import GridHelper
from py3d.extras.movement_rig import MovementRig
from py3d.material.surface import SurfaceMaterial


class Example(Base):
    """
    Render axes, a rotated xy-grid, and a box.
    Move the box: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 1, 5])
        geometry = BoxGeometry()
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.mesh = Mesh(geometry, material)
        self.rig = MovementRig()
        self.rig.add(self.mesh)
        self.rig.set_position([0, 0.5, 0])
        self.scene.add(self.rig)
        axes = AxesHelper(axis_length=2)
        self.scene.add(axes)
        grid = GridHelper(
            size=20,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0]
        )
        grid.rotate_x(-math.pi / 2)
        self.scene.add(grid)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
