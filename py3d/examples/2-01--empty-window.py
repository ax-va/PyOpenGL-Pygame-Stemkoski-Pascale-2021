#!/usr/bin/python3
import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from py3d.core.base import Base


class Example(Base):
    """ Render a window """
    def initialize(self):
        print("Initializing program...")

    def update(self):
        pass


# Instantiate this class and run the program
Example().run()