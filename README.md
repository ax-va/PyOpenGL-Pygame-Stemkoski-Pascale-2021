# OpenGL examples with PyOpenGL and Pygame
The OpenGL examples are based on book *"Developing Graphics Frameworks with Python and OpenGL"* by Lee Stemkoski and Michael Pascale published by *CRC Press* in 2021. 

The examples cover all the book chapters with code, 2 through 6, with some code changes and demonstrate **GLSL** programming using **PyOpenGL**. **Pygame** is mainly used for control, windowing, and image loading.

You find the examples in the `examples` folder. Just read a class description in a script and run it. Since the object-oriented approach is used, auxiliary classes are logically separated in other folders (packages).

My environment was Python 3.8 with the following packages (without specifying their dependencies here):
```
numpy==1.22.4
pygame==2.1.2
PyOpenGL==3.1.6
PyOpenGL-accelerate==3.1.6
```

The code was tested on the same machine with two operating systems, more precisely:

- OS: Windows 11; Vendor: ATI Technologies Inc.; Renderer: AMD Radeon(TM) Graphics; OpenGL version supported: 4.6.14761 Compatibility Profile Context 21.30.44.03 30.0.13044.3001; GLSL version supported: 4.60

- OS: Ubuntu 20.04.3 LTS; Vendor: AMD; Renderer: AMD RENOIR (DRM 3.41.0, 5.13.0-48-generic, LLVM 12.0.0); OpenGL version supported: 4.6 (Compatibility Profile) Mesa 21.2.6; GLSL version supported: 4.60

Update:

- On Ubuntu, you can get an error `OpenGL.error.Error: Attempt to retrieve context when no valid context`. See a bug report and suggestions to resolve it: https://github.com/pygame/pygame/issues/3110
