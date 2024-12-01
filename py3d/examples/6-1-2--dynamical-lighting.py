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
from py3d.extras.directional_light import DirectionalLightHelper
from py3d.extras.movement_rig import MovementRig
from py3d.extras.point_light import PointLightHelper
from py3d.geometry.sphere import SphereGeometry
from py3d.light.ambient import AmbientLight
from py3d.light.directional import DirectionalLight
from py3d.light.point import PointLight
from py3d.material.flat import FlatMaterial
from py3d.material.lambert import LambertMaterial
from py3d.material.phong import PhongMaterial


class Example(Base):
    """
    Demonstrate dynamical lighting with:
    - the flat shading model;
    - the Lambert illumination model and Phong shading model;
    - the Phong illumination model and Phong shading model;
    and render light helpers that show a light position and
    a light direction for a point light and a directional light,
    respectively.

    Move a camera: WASDRF(move), QE(turn), TG(look).
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 0, 6])
        self.scene.add(self.rig)

        # three light sources
        ambient_light = AmbientLight(color=[0.1, 0.1, 0.1])
        self.scene.add(ambient_light)
        self.directional_light = DirectionalLight(color=[0.8, 0.8, 0.8], direction=[-1, -1, 0])
        self.scene.add(self.directional_light)
        self.point_light = PointLight(color=[0.9, 0, 0], position=[1, 1, 0.8])
        self.scene.add(self.point_light)

        # lighted materials with a color
        flat_material = FlatMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=3
        )
        lambert_material = LambertMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=3
        )
        phong_material = PhongMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=3
        )

        # lighted spheres with a color
        sphere_geometry = SphereGeometry()
        sphere_left = Mesh(sphere_geometry, flat_material)
        sphere_left.set_position([-2.5, 0, 0])
        self.scene.add(sphere_left)
        sphere_center = Mesh(sphere_geometry, lambert_material)
        sphere_center.set_position([0, 0, 0])
        self.scene.add(sphere_center)
        sphere_right = Mesh(sphere_geometry, phong_material)
        sphere_right.set_position([2.5, 0, 0])
        self.scene.add(sphere_right)

        # helpers
        directional_light_helper = DirectionalLightHelper(self.directional_light)
        # The directional light can take any position because it covers all the space.
        # The directional light helper is a child of the directional light.
        # So changing the global matrix of the parent leads to changing
        # the global matrix of its child.
        self.directional_light.set_position([0, 2, 0])
        self.directional_light.add(directional_light_helper)
        point_light_helper = PointLightHelper(self.point_light)
        self.point_light.add(point_light_helper)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.directional_light.set_direction([-1, math.sin(0.5 * self.time), 0])
        self.point_light.set_position([1, math.sin(self.time), 1])
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
