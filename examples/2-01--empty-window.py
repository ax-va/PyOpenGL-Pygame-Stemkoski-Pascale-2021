#!/usr/bin/python3
from py3d.core.base import Base


class Example(Base):
    """ Render a window """
    def initialize(self):
        print("Initializing program...")

    def update(self):
        pass


# Instantiate this class and run the program
Example().run()