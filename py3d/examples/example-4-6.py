import numpy as np
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
from py3d.extras.axes import AxesHelper
from py3d.extras.grid import GridHelper
from py3d.extras.movement_rig import MovementRig


class Example(Base):
    """
    Render the axes and the rotated xy-grid.
    Add camera movement: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self._renderer = Renderer()
        self._scene = Scene()
        self._camera = Camera(aspect_ratio=800/600)
        self._rig = MovementRig()
        self._rig.add(self._camera)
        self._rig.set_position([0.5, 1, 5])
        self._scene.add(self._rig)
        axes = AxesHelper(axis_length=2)
        self._scene.add(axes)
        grid = GridHelper(
            size=20,
            grid_color=[1, 1, 1],
            center_color=[1, 1, 0]
        )
        grid.rotate_x(-math.pi / 2)
        self._scene.add(grid)

    def update(self):
        self._rig.update(self._input, self._delta_time)
        self._renderer.render(self._scene, self._camera)


# Instantiate this class and run the program
Example(screen_size=[800,600]).run()
