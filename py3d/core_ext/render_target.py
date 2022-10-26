import OpenGL.GL as GL
import pygame

from py3d.core_ext.texture import Texture


class RenderTarget:
    """
    Create a framebuffer as the target when rendering
    """
    def __init__(self, resolution=(512, 512), texture=None, property_dict=None):
        # Values should equal texture dimensions
        self._width, self._height = resolution
        if texture is not None:
            self._texture = texture
        else:
            self._texture = Texture(
                file_name=None,
                property_dict={
                    "magFilter": GL.GL_LINEAR,
                    "minFilter": GL.GL_LINEAR,
                    "wrap": GL.GL_CLAMP_TO_EDGE
                }
            )
            self._texture.set_properties(property_dict)
            self._texture.surface = pygame.Surface(resolution)
            self._texture.upload_data()
        # Create a framebuffer
        self._framebuffer_ref = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._framebuffer_ref)
        # Configure color buffer to use this texture
        GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0,
                                self._texture.texture_ref, 0)
        # Generate a buffer to store depth information
        depth_buffer_ref = GL.glGenRenderbuffers(1)
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, depth_buffer_ref)
        GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT, self._width, self._height)
        GL.glFramebufferRenderbuffer(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_RENDERBUFFER, depth_buffer_ref)
        # Check framebuffer status
        if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
            raise Exception("Framebuffer status error")

    @property
    def framebuffer_ref(self):
        return self._framebuffer_ref

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def texture(self):
        return self._texture
