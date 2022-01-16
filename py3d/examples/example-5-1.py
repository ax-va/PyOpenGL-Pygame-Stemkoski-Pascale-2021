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
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.texture import TextureMaterial


class Example(Base):
    """ Render a rectangle with a texture applied to it """
    def initialize(self):
        print("Initializing program...")
        self._renderer = Renderer()
        self._scene = Scene()
        self._camera = Camera(aspect_ratio=800/600)
        self._camera.set_position([0, 0, 2])
        geometry = RectangleGeometry()
        grid = Texture("../images/grid.jpg")
        material = TextureMaterial(grid)
        self._mesh = Mesh(geometry, material)
        self._scene.add(self._mesh)

    def update(self):
        self._renderer.render(self._scene, self._camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
