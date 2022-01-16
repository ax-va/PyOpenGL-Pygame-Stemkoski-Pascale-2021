import OpenGL.GL as GL

from collections import namedtuple


class Utils:
    """
    Static methods to load and compile OpenGL shaders and link to create programs
    """
    @staticmethod
    def get_system_info():
        vendor = GL.glGetString(GL.GL_VENDOR).decode('utf-8')
        renderer = GL.glGetString(GL.GL_RENDERER).decode('utf-8')
        opengl = GL.glGetString(GL.GL_VERSION).decode('utf-8')
        glsl = GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('utf-8')
        Result = namedtuple('SystemInfo', ['vendor', 'renderer', 'opengl', 'glsl'])
        return Result(vendor, renderer, opengl, glsl)

    @staticmethod
    def initialize_shader(shader_code, shader_type):
        # Specify required OpenGL/GLSL version
        shader_code = '#version 330\n' + shader_code
        # Create empty shader object and return reference value
        shader_ref = GL.glCreateShader(shader_type)
        # Stores the source code in the shader
        GL.glShaderSource(shader_ref, shader_code)
        # Compiles source code previously stored in the shader object
        GL.glCompileShader(shader_ref)
        # Queries whether shader compile was successful
        compile_success = GL.glGetShaderiv(shader_ref, GL.GL_COMPILE_STATUS)
        if not compile_success:
            # Retrieve error message
            error_message = GL.glGetShaderInfoLog(shader_ref)
            # free memory used to store shader program
            GL.glDeleteShader(shader_ref)
            # Convert byte string to character string
            error_message = '\n' + error_message.decode('utf-8')
            # Raise exception: halt program and print error message
            raise Exception(error_message)
        # Compilation was successful; return shader reference value
        return shader_ref

    @staticmethod
    def initialize_program(vertex_shader_code, fragment_shader_code):
        vertex_shader_ref = Utils.initialize_shader(vertex_shader_code, GL.GL_VERTEX_SHADER)
        fragment_shader_ref = Utils.initialize_shader(fragment_shader_code, GL.GL_FRAGMENT_SHADER)
        # Create empty program object and store reference to it
        program_ref = GL.glCreateProgram()
        # Attach previously compiled shader programs
        GL.glAttachShader(program_ref, vertex_shader_ref)
        GL.glAttachShader(program_ref, fragment_shader_ref)
        # Link vertex shader to fragment shader
        GL.glLinkProgram(program_ref)
        # queries whether program link was successful
        link_success = GL.glGetProgramiv(program_ref, GL.GL_LINK_STATUS)
        if not link_success:
            # Retrieve error message
            error_message = GL.glGetProgramInfoLog(program_ref)
            # free memory used to store program
            GL.glDeleteProgram(program_ref)
            # Convert byte string to character string
            error_message = '\n' + error_message.decode('utf-8')
            # Raise exception: halt application and print error message
            raise Exception(error_message)
        # Linking was successful; return program reference value
        return program_ref

    @staticmethod
    def print_system_info():
        info = Utils.get_system_info()
        result = ''.join(['Vendor: ', info.vendor, '\n',
                          'Renderer: ', info.renderer, '\n',
                          'OpenGL version supported: ', info.opengl, '\n',
                          'GLSL version supported: ', info.glsl])
        print(result)
