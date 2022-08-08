import OpenGL.GL as GL

from py3d.core_ext.camera import Camera
from py3d.core_ext.render_target import RenderTarget
from py3d.material.depth import DepthMaterial


class Shadow:
    def __init__(self,
                 light_source,
                 strength=0.5,
                 resolution=(512, 512),
                 camera_bounds=(-5, 5, -5, 5, 0, 20),
                 bias=0.01):

        # Must be directional light
        self._light_source = light_source
        # Camera used to render scene from perspective of light
        self._camera = Camera()
        left, right, bottom, top, near, far = camera_bounds
        self._camera.set_orthographic(left, right, bottom, top, near, far)
        self._light_source.add(self._camera)
        # Target used during the shadow pass, contains depth texture
        self._render_target = RenderTarget(
            resolution,
            property_dict={"wrap": GL.GL_CLAMP_TO_BORDER}
        )
        # Render only depth data to target texture
        self._material = DepthMaterial()
        # Controls darkness of shadow
        self._strength = strength
        # Used to avoid visual artifacts due to
        # rounding / sampling precision issues
        self._bias = bias

    @property
    def bias(self):
        return self._bias

    @property
    def camera(self):
        return self._camera

    @property
    def material(self):
        return self._material

    @property
    def light_source(self):
        return self._light_source

    @property
    def render_target(self):
        return self._render_target

    @property
    def strength(self):
        return self._strength

    def update_internal(self):
        self._camera.update_view_matrix()
        self._material.uniform_dict["viewMatrix"].data = self._camera.view_matrix
        self._material.uniform_dict["projectionMatrix"].data = self._camera.projection_matrix
