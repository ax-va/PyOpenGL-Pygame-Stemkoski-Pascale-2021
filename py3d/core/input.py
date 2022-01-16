import pygame


class Input:
    def __init__(self):
        # Has the user quit the application?
        self._quit = False
        # lists to store key states
        # down, up: discrete event; lasts for one iteration
        # pressed: continuous event, between down and up events
        self._key_down_list = []
        self._key_pressed_list = []
        self._key_up_list = []

    @property
    def key_down_list(self):
        return self._key_down_list

    @property
    def key_pressed_list(self):
        return self._key_pressed_list

    @property
    def key_up_list(self):
        return self._key_up_list

    @property
    def quit(self):
        return self._quit

    # functions to check key states
    def is_key_down(self, key_code):
        return key_code in self._key_down_list

    def is_key_pressed(self, key_code):
        return key_code in self._key_pressed_list

    def is_key_up(self, key_code):
        return key_code in self._key_up_list

    def update(self):
        # Reset discrete key states
        self._key_down_list = []
        self._key_up_list = []
        # Iterate over all user input events (such as keyboard or mouse)
        # that occurred since the last time events were checked
        for event in pygame.event.get():
            # Quit event occurs by clicking button to close window
            if event.type == pygame.QUIT:
                self._quit = True
            # Check for key-down and key-up events;
            # get name of key from event and append to or remove from corresponding lists
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                self._key_down_list.append(key_name)
                self._key_pressed_list.append(key_name)
            if event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                self._key_pressed_list.remove(key_name)
                self._key_up_list.append(key_name)