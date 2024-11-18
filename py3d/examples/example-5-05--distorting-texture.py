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
    """ Distort a texture over time by using a RGB noise texture with pseudo-random uv-coordinates """
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
            uniform sampler2D rgbNoiseSampler;
            uniform sampler2D imageSampler;
            in vec2 UV;
            uniform float time;
            out vec4 fragColor;

            void main()
            {
                vec2 uvShift = UV + vec2(-0.033, 0.07) * time;
                vec4 noiseValues = texture(rgbNoiseSampler, uvShift);
                vec2 uvNoise = UV + 0.01 * noiseValues.rg;
                fragColor = texture(imageSampler, uvNoise);
            }
        """
        rgb_noise_texture = Texture("../images/rgb-noise.jpg")
        grid_texture = Texture("../images/grid.jpg")
        self.distort_material = Material(vertex_shader_code, fragment_shader_code)
        self.distort_material.add_uniform("sampler2D", "rgbNoiseSampler", [rgb_noise_texture.texture_ref, 1])
        self.distort_material.add_uniform("sampler2D", "imageSampler", [grid_texture.texture_ref, 2])
        self.distort_material.add_uniform("float", "time", 0.0)
        self.distort_material.locate_uniforms()

        geometry = RectangleGeometry()
        self.mesh = Mesh(geometry, self.distort_material)
        self.scene.add(self.mesh)

    def update(self):
        self.distort_material.uniform_dict["time"].data += self.delta_time
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
