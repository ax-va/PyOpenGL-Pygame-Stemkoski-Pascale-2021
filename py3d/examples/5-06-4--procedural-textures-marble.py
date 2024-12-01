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
from py3d.geometry.rectangle import RectangleGeometry
from py3d.material.material import Material


class Example(Base):
    """
    Generate a procedural fragment color by using uv-coordinates
    and also clouds, lava, marble, and wood grain textures
    """

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)
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
                vec4 pos = vec4(vertexPosition, 1.0);
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * pos;
                UV = vertexUV;
            }
        """
        fragment_shader_code = """
            // Return a random value in [0, 1]
            float random(vec2 UV)
            {
                return fract(235711.0 * sin(14.337 * UV.x + 42.418 * UV.y));
            }

            float boxRandom(vec2 UV, float scale)
            {
                vec2 iScaleUV = floor(scale * UV);
                return random(iScaleUV);
            }

            float smoothRandom(vec2 UV, float scale)
            {
                vec2 iScaleUV = floor(scale * UV);
                vec2 fScaleUV = fract(scale * UV);
                float a = random(iScaleUV);
                float b = random(round(iScaleUV + vec2(1, 0)));
                float c = random(round(iScaleUV + vec2(0, 1)));
                float d = random(round(iScaleUV + vec2(1, 1)));
                return mix(mix(a, b, fScaleUV.x), mix(c, d, fScaleUV.x), fScaleUV.y);
            }

            // Add smooth random values at different scales
            // weighted (amplitudes) so that sum is approximately 1.0
            float fractalLikeRandom(vec2 UV, float scale)
            {
                float value = 0.0;
                float amplitude = 0.5;
                for (int i = 0; i < 10; i++)
                {
                    value += amplitude * smoothRandom(UV, scale);
                    scale *= 2.0;
                    amplitude *= 0.5;
                }
                return value;
            }

            in vec2 UV;
            out vec4 fragColor;
            void main()
            {
                // marble
                float t = fractalLikeRandom(UV, 4);
                float r = abs(sin(20 * t));
                vec4 color1 = vec4(0.0, 0.2, 0.0, 1.0);
                vec4 color2 = vec4(1.0, 1.0, 1.0, 1.0);
                fragColor = mix(color1, color2, r);    
            }
        """
        material = Material(vertex_shader_code, fragment_shader_code)
        material.locate_uniforms()

        geometry = RectangleGeometry()
        mesh = Mesh(geometry, material)
        self.scene.add(mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)


# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
