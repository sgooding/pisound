import pygame
import glob
import os

from signal import pause
import time

from pisound.convert import automount_usb, convert
from pisound.state import State
from pisound import __version__

states = dict()

automount_usb()

convert()

pygame.mixer.init()

def button_pressed(button):
    if button.value == 1:
        states[button.pin].toggle()

def startup():
    startup = os.path.join(MEDIA_PATH,"startup","startup.wav")
    print(f'playing: {startup}')
    startup_sound = pygame.mixer.Sound(startup)
    startup_sound.play()

def shutdown_pi():
    print('Good Bye')
    shutdown = os.path.join(MEDIA_PATH,"startup","shutdown.wav")

    pygame.mixer.stop()

    shutdown_sound = pygame.mixer.Sound(shutdown)
    shutdown_sound.play()
    time.sleep(15)
    os.system('sudo shutdown -h now')


MEDIA_PATH=os.environ.get('MEDIA_PATH','/home/pi/media')

if not os.path.exists(MEDIA_PATH):
    raise FileNotFoundError('Could not find media path file.')

startup()

# Assign Buttons
files = glob.glob(os.path.join(MEDIA_PATH,"*.wav"))
gpio_pins = [2,3,4,17]
for file, gpi_pin in zip(files[0:4],gpio_pins):
    state = State(file, gpi_pin)
    state.button.when_pressed = button_pressed
    state.button.when_held = shutdown_pi
    states[state.button.pin] = state

print(f'Welcome to PiSound {__version__}')
pause()
