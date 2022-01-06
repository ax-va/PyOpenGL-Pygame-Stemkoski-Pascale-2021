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
# from py3d.geometry.geometry import Geometry
from py3d.material.surface import SurfaceMaterial


class Example(Base):
    """ Render a basic scene that consists of a spinning cube """
    def initialize(self):
        print("Initializing program...")
        self._renderer = Renderer()
        self._scene = Scene()
        self._camera = Camera(aspect_ratio=800/600)
        self._camera.set_position([0, 0, 4])
        geometry = BoxGeometry()
        # material = SurfaceMaterial({"useVertexColors": True})
        material = SurfaceMaterial(
            {
                "useVertexColors": True,
                "wireframe": True,
                "lineWidth": 8
            }
        )
        self._mesh = Mesh(geometry, material)
        self._scene.add(self._mesh)

    def update(self):
        # self._mesh.rotate_y(0.0514)
        # self._mesh.rotate_x(0.0337)
        self._renderer.render(self._scene, self._camera)


# Instantiate this class and run the program
Example(screen_size=[800,600]).run()