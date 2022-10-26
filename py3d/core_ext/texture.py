import OpenGL.GL as GL
import pygame


class Texture:
    def __init__(self, file_name=None, property_dict={}):
        # Pygame object for storing pixel data;
        # can load from image or manipulate directly
        self._surface = None
        # reference of available texture from GPU
        self._texture_ref = GL.glGenTextures(1)
        # default property values
        self._property_dict = {
            "magFilter": GL.GL_LINEAR,
            "minFilter": GL.GL_LINEAR_MIPMAP_LINEAR,
            "wrap": GL.GL_REPEAT
        }
        # Overwrite default property values
        self.set_properties(property_dict)
        if file_name is not None:
            self.load_image(file_name)
            self.upload_data()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface

    @property
    def texture_ref(self):
        return self._texture_ref

    def load_image(self, file_name):
        """ Load image from file """
        self._surface = pygame.image.load(file_name)

    def set_properties(self, property_dict):
        """ Set property values """
        if property_dict:
            for name, value in property_dict.items():
                if name in self._property_dict.keys():
                    self._property_dict[name] = value
                else:  # unknown property type
                    raise Exception("Texture has no property with name: " + name)

    def upload_data(self):
        """ Upload pixel data to GPU """
        # Store image dimensions
        width = self._surface.get_width()
        height = self._surface.get_height()
        # Convert image data to string buffer
        pixel_data = pygame.image.tostring(self._surface, "RGBA", True)
        # Specify texture used by the following functions
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture_ref)
        # Send pixel data to texture buffer
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, pixel_data)
        # Generate mipmap image from uploaded pixel data
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
        # Specify technique for magnifying/minifying textures
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, self._property_dict["magFilter"])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, self._property_dict["minFilter"])
        # Specify what happens to texture coordinates outside range [0, 1]
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, self._property_dict["wrap"])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, self._property_dict["wrap"])
        # Set default border color to white; important for rendering shadows
        GL.glTexParameterfv(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_BORDER_COLOR, [1, 1, 1, 1])