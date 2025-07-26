#!/usr/bin/python3
from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.core_ext.texture import Texture
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.texture import TextureMaterial


class Example(Base):
    """ Render a textured square """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 2])
        geometry = RectangleGeometry()
        grid_texture = Texture(file_name="../py3d/images/grid.jpg")
        material = TextureMaterial(texture=grid_texture)
        self.mesh = Mesh(
            geometry=geometry,
            material=material
        )
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
