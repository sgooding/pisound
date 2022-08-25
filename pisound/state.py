import pygame
from gpiozero import Button
import time

class State:
    CHANNEL_ID = 0

    def __init__(self, file, gpio_pin) -> None:

        State.CHANNEL_ID += 1

        self.file = file
        self.gpio_pin = gpio_pin

        self.button = Button( self.gpio_pin, 
                              pull_up=True,
                              hold_time=5 )
        self.sound = pygame.mixer.Sound(self.file)

        self._last_toggle = time.time()
        self._channel = pygame.mixer.Channel(self.CHANNEL_ID)

    def update(self):
        if ( self._channel.get_busy() ):
            print(f"stopping: {self.file}")
            self._channel.stop()
        else:
            print(f"playing : {self.file}")
            self._channel.play(self.sound)

    def toggle(self):
        now = time.time()
        if (now-self._last_toggle) > 0.5:
            #self.state = not self.state
            self._last_toggle = now
            self.update()
            print(f'Toggle: \n {self}')

        

    def __repr__(self):
        return f'''
        State:
            gpio        : {self.gpio_pin}
            file        : {self.file}
            buttn       : {self.button.value}
            is_playing  : {self._channel.get_busy()}
        '''