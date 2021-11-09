from opengl_tutorial.core.base import Base


# check input
class Test(Base):
    """ Create a text-based application to verify that these modifications work as expected """
    def initialize(self):
        print("Initializing program...")

    def update(self):
        # # debug printing
        # if len(self._input.key_down_list) > 0:
        #     print('Keys down:', self._input.key_down_list)
        # if len(self._input.key_pressed_list) > 0:
        #     print('Keys pressed:', self._input.key_pressed_list)
        # if len(self._input.key_up_list) > 0:
        #     print('Keys up:', self._input.key_up_list)
        # typical usage
        if self._input.is_key_down('space'):
            print("The 'space' key was just pressed down")
        if self._input.is_key_pressed('right'):
            print("The 'right' key is currently being pressed")


# instantiate this class and run the program
Test().run()