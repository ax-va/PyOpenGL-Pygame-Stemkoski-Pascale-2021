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
from py3d.core_ext.texture import Texture
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.material import Material


class Example(Base):
    """
    Blend between two different textures cyclically.  The fragment shader
    samples colors from two textures at each fragment, and then, linearly
    interpolates between these colors to determine the output fragment color.
    """
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 1.5])
        vertex_shader_code = """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec2 vertexUV;
            out vec2 UV;

            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                UV = vertexUV;
            }
        """
        fragment_shader_code = """
            uniform sampler2D textureSampler1;
            uniform sampler2D textureSampler2;
            in vec2 UV;
            uniform float time;
            out vec4 fragColor;

            void main()
            {
                vec4 color1 = texture(textureSampler1, UV);
                vec4 color2 = texture(textureSampler2, UV);
                float s = abs(sin(time));
                fragColor = s * color1 + (1.0 - s) * color2;
            }
        """
        grid_texture = Texture("../images/grid.jpg")
        crate_texture = Texture("../images/crate.jpg")
        self.blend_material = Material(vertex_shader_code, fragment_shader_code)
        self.blend_material.add_uniform("sampler2D", "textureSampler1", [grid_texture.texture_ref, 1])
        self.blend_material.add_uniform("sampler2D", "textureSampler2", [crate_texture.texture_ref, 2])
        self.blend_material.add_uniform("float", "time", 0.0)
        self.blend_material.locate_uniforms()

        geometry = RectangleGeometry()
        self.mesh = Mesh(geometry, self.blend_material)
        self.scene.add(self.mesh)

    def update(self):
        self.blend_material.uniform_dict["time"].data += self.delta_time
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
