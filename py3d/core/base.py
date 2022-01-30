import pygame
import sys

from py3d.core.input import Input
from py3d.core.utils import Utils


class Base:
    def __init__(self, screen_size=(512, 512)):
        # Initialize all pygame modules
        pygame.init()
        # Indicate rendering details
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL
        # Initialize buffers to perform antialiasing
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        # Use a core OpenGL profile for cross-platform compatibility
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        # Create and display the window
        self._screen = pygame.display.set_mode(screen_size, display_flags)
        # Set the text that appears in the title bar of the window
        pygame.display.set_caption("Graphics Window")
        # Determine if main loop is active
        self._running = True
        # Manage time-related data and operations
        self._clock = pygame.time.Clock()
        # Manage user input
        self._input = Input()
        # number of seconds application has been running
        self._time = 0
        # Print the system information
        Utils.print_system_info()

    @property
    def delta_time(self):
        return self._delta_time

    @property
    def input(self):
        return self._input

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def initialize(self):
        """ Implement by extending class """
        pass

    def update(self):
        """ Implement by extending class """
        pass

    def run(self):
        # Startup #
        self.initialize()
        # main loop #
        while self._running:
            # process input #
            self._input.update()
            if self._input.quit:
                self._running = False
            # seconds since iteration of run loop
            self._delta_time = self._clock.get_time() / 1000
            # Increment time application has been running
            self._time += self._delta_time
            # Update #
            self.update()
            # Render #
            # Display image on screen
            pygame.display.flip()
            # Pause if necessary to achieve 60 FPS
            self._clock.tick(60)
        # Shutdown #
        pygame.quit()
        sys.exit()
