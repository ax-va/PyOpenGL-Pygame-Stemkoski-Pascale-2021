from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.render_target import RenderTarget
from py3d.geometry.geometry import Geometry


class Postprocessor:
    """
    Create effects by postprocessing
    """
    def __init__(self,
                 renderer: Renderer,
                 scene: Scene,
                 camera: Camera,
                 final_render_target=None):
        self._renderer = renderer
        self._scene_list = [scene]
        self._camera_list = [camera]
        self._render_target_list = [final_render_target]
        self._final_render_target = final_render_target
        self._ortho_camera = Camera()
        self._ortho_camera.set_orthographic()  # aligned with clip space
        # By default, generate a rectangle already aligned with clip space;
        # no matrix transformations will be applied
        self._rectangle_geometry = Geometry()
        p0, p1, p2, p3 = [-1, -1], [1, -1], [-1, 1], [1, 1]
        t0, t1, t2, t3 = [0, 0], [1, 0], [0, 1], [1, 1]
        position_data = [p0, p1, p3, p0, p3, p2]
        uv_data = [t0, t1, t3, t0, t3, t2]
        self._rectangle_geometry.add_attribute("vec2", "vertexPosition", position_data)
        self._rectangle_geometry.add_attribute("vec2", "vertexUV", uv_data)

    @property
    def render_target_list(self):
        return self._render_target_list

    def add_effect(self, effect):
        post_scene = Scene()
        resolution = self._renderer.window_size
        target = RenderTarget(resolution=resolution)
        # Change the previous entry in the render target list
        # to this newly created render target
        self._render_target_list[-1] = target
        # The effect in this render pass will use the texture
        # that was written to in the previous render pass
        effect.uniform_dict["textureSampler"].data[0] = target.texture.texture_ref
        mesh = Mesh(self._rectangle_geometry, effect)
        post_scene.add(mesh)
        self._scene_list.append(post_scene)
        self._camera_list.append(self._ortho_camera)
        self._render_target_list.append(self._final_render_target)

    def render(self):
        passes = len(self._scene_list)
        for n in range(passes):
            scene = self._scene_list[n]
            camera = self._camera_list[n]
            target = self._render_target_list[n]
            self._renderer.render(scene, camera, render_target=target)
