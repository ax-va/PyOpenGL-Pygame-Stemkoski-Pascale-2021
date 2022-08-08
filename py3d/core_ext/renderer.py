import OpenGL.GL as GL
import pygame

from py3d.core_ext.mesh import Mesh
from py3d.light.light import Light
from py3d.light.shadow import Shadow


class Renderer:
    def __init__(self, clear_color=(0, 0, 0)):
        GL.glEnable(GL.GL_DEPTH_TEST)
        # required for antialiasing
        GL.glEnable(GL.GL_MULTISAMPLE)
        GL.glClearColor(*clear_color, 1)
        self._window_size = pygame.display.get_surface().get_size()
        self._shadows_enabled = False

    @property
    def window_size(self):
        return self._window_size

    @property
    def shadow_object(self):
        return self._shadow_object

    def render(self, scene, camera, clear_color=True, clear_depth=True, render_target=None):
        # Filter descendents
        descendant_list = scene.descendant_list
        mesh_filter = lambda x: isinstance(x, Mesh)
        mesh_list = list(filter(mesh_filter, descendant_list))

        # shadow pass
        if self._shadows_enabled:
            # Set render target properties
            GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._shadow_object.render_target.framebuffer_ref)
            GL.glViewport(0, 0, self._shadow_object.render_target.width, self._shadow_object.render_target.height)
            # Set default color to white, used when no objects present to cast shadows
            GL.glClearColor(1, 1, 1, 1)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            GL.glClear(GL.GL_DEPTH_BUFFER_BIT)
            # Everything in the scene gets rendered with depthMaterial so
            # only need to call glUseProgram & set matrices once
            GL.glUseProgram(self._shadow_object.material.program_ref)
            self._shadow_object.update_internal()
            for mesh in mesh_list:
                # Skip invisible meshes
                if not mesh.visible:
                    continue
                # Only triangle-based meshes cast shadows
                if mesh.material.setting_dict["drawStyle"] != GL.GL_TRIANGLES:
                    continue
                # Bind VAO
                GL.glBindVertexArray(mesh.vao_ref)
                # Update transform data
                self._shadow_object.material.uniform_dict["modelMatrix"].data = mesh.global_matrix
                # Update uniforms (matrix data) stored in shadow material
                for var_name, uniform_obj in self._shadow_object.material.uniform_dict.items():
                    uniform_obj.upload_data()
                GL.glDrawArrays(GL.GL_TRIANGLES, 0, mesh.geometry.vertex_count)

        # Activate render target
        if render_target is None:
            # Set render target to window
            # (the value 0 is indicating the framebuffer attached to the window)
            GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
            GL.glViewport(0, 0, *self._window_size)
        else:
            # Set render target properties
            GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, render_target.framebuffer_ref)
            GL.glViewport(0, 0, render_target.width, render_target.height)
        # Clear color and depth buffers
        # GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        if clear_color:
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        if clear_depth:
            GL.glClear(GL.GL_DEPTH_BUFFER_BIT)
        # blending
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        # Update camera view (calculate inverse)
        camera.update_view_matrix()
        # Extract list of all Mesh instances in scene
        descendant_list = scene.descendant_list
        mesh_list = list(filter(lambda x: isinstance(x, Mesh), descendant_list))
        # Extract list of all Light instances in scene
        light_list = list(filter(lambda x: isinstance(x, Light), descendant_list))
        for mesh in mesh_list:
            # If this object is not visible, continue to next object in list
            if not mesh.visible:
                continue
            GL.glUseProgram(mesh.material.program_ref)
            # Bind VAO
            GL.glBindVertexArray(mesh.vao_ref)
            # Update uniform values stored outside of material
            mesh.material.uniform_dict["modelMatrix"].data = mesh.global_matrix
            mesh.material.uniform_dict["viewMatrix"].data = camera.view_matrix
            mesh.material.uniform_dict["projectionMatrix"].data = camera.projection_matrix
            # If material uses light data, add lights from list
            if "light0" in mesh.material.uniform_dict.keys():
                for light_number in range(len(light_list)):
                    light_name = "light" + str(light_number)
                    light_instance = light_list[light_number]
                    mesh.material.uniform_dict[light_name].data = light_instance
            # Add camera position if needed (specular lighting)
            if "viewPosition" in mesh.material.uniform_dict.keys():
                mesh.material.uniform_dict["viewPosition"].data = camera.global_position
            # Add shadow data if enabled and used by shader
            if self._shadows_enabled and "shadow0" in mesh.material.uniform_dict.keys():
                mesh.material.uniform_dict["shadow0"].data = self._shadow_object
            # Update uniforms stored in material
            for uniform_object in mesh.material.uniform_dict.values():
                uniform_object.upload_data()
            # Update render settings
            mesh.material.update_render_settings()
            GL.glDrawArrays(mesh.material.setting_dict["drawStyle"], 0, mesh.geometry.vertex_count)

    def enable_shadows(self, shadow_light, strength=0.5, resolution=(512, 512)):
        self._shadows_enabled = True
        self._shadow_object = Shadow(shadow_light, strength=strength, resolution=resolution)
