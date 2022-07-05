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
from py3d.core_ext.texture import Texture
from py3d.geometry.rectangle import RectangleGeometry
from py3d.extras.point_light import PointLightHelper
from py3d.light.ambient import AmbientLight
from py3d.light.point import PointLight
from py3d.material.lambert import LambertMaterial


class Example(Base):
    """ Bump mapping: combining color textures with normal map textures """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 2])

        ambient_light = AmbientLight(color=[0.3, 0.3, 0.3])
        self.scene.add(ambient_light)
        self.point_light = PointLight(color=[1, 1, 1], position=[1, 0, 1])
        self.scene.add(self.point_light)
        # texture of a brick wall
        color_texture = Texture("../images/brick-wall.jpg")
        # texture of normals of the brick wall
        bump_texture = Texture("../images/brick-wall-normal-map.jpg")

        rectangle_geometry = RectangleGeometry(width=2, height=2)

        color_material = LambertMaterial(
            texture=color_texture,
            number_of_light_sources=2
        )

        bump_material = LambertMaterial(
            texture=color_texture,
            bump_texture=bump_texture,
            property_dict={"bumpStrength": 1},
            number_of_light_sources=2
        )

        # Replace color_material and bump_material
        # in Mesh to see a difference
        mesh = Mesh(rectangle_geometry, bump_material)
        self.scene.add(mesh)

        point_light_helper = PointLightHelper(self.point_light)
        self.point_light.add(point_light_helper)

    def update(self):
        self.point_light.set_position([math.cos(0.5 * self.time) / 2, math.sin(0.5 * self.time) / 2, 1])
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
