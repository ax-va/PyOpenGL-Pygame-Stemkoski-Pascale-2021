import pygame
import sys

from opengl_tutorial.core.input import Input
from opengl_tutorial.core.utils import Utils


class Base(object):
    def __init__(self, screen_size=(512, 512)):
        # initialize all pygame modules
        pygame.init()
        # indicate rendering details
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL
        # initialize buffers to perform antialiasing
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        # use a core OpenGL profile for cross-platform compatibility
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        # create and display the window
        self._screen = pygame.display.set_mode(screen_size, display_flags)
        # set the text that appears in the title bar of the window
        pygame.display.set_caption("Graphics Window")
        # determine if main loop is active
        self._running = True
        # manage time-related data and operations
        self._clock = pygame.time.Clock()
        # manage user input
        self._input = Input()
        # print the system information
        Utils.print_system_info()

    # implement by extending class
    def initialize(self):
        pass

    # implement by extending class
    def update(self):
        pass

    def run(self):
        # startup #
        self.initialize()
        # main loop #
        while self._running:
            # process input #
            self._input.update()
            if self._input.quit:
                self._running = False
            # update #
            self.update()
            # render #
            # display image on screen
            pygame.display.flip()
            # pause if necessary to achieve 60 FPS
            self._clock.tick(60)
        # shutdown #
        pygame.quit()
        sys.exit()
