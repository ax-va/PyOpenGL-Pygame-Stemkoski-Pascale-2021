#!/usr/bin/python3
import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from py3d.core.base import Base


# Check input
class Example(Base):
    """ Create a text-based application to verify that the key press works as expected """
    def initialize(self):
        print("Initializing program...")

    def update(self):
        if self.input.is_key_down('space'):
            print("The 'space' key was just pressed down")
        if self.input.is_key_up('space'):
            print("The 'space' key was just pressed up")
        if self.input.is_key_pressed('right'):
            print("The 'right' key is currently being pressed")


# Instantiate this class and run the program
Example().run()
