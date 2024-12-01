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
from py3d.geometry.geometry import Geometry
from py3d.material.surface import SurfaceMaterial


class Example(Base):
    """ Render a basic scene that consists of a custom geometry """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 0.5])
        geometry = Geometry()
        p0 = [-0.1, 0.1, 0.0]
        p1 = [0.0, 0.0, 0.0]
        p2 = [0.1, 0.1, 0.0]
        p3 = [-0.2, -0.2, 0.0]
        p4 = [0.2, -0.2, 0.0]
        position_data = [p0, p3, p1, p1, p3, p4, p1, p4, p2]
        geometry.add_attribute("vec3", "vertexPosition", position_data)
        R = [1, 0, 0]
        Y = [1, 1, 0]
        G = [0, 0.25, 0]
        color_data = [R, G, Y, Y, G, G, Y, G, R]
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()