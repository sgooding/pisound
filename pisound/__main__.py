import pygame
import glob
import os

from gpiozero import Button
from signal import pause

from .convert import convert

print('Convert Mp3 to Wav Files')
convert()

print('Initialize pygame mixer')
pygame.mixer.init()

channels = dict()
assigned_sounds = dict()

def button_pressed(button):
    global sounds
    global channels

    if button.pin in channels:
        is_busy = channels[button.pin].get_busy()
        print(f'Stop Playing: {assigned_sounds[button.pin]}')
        if is_busy:
            channels[button.pin].stop()
            del channels[button.pin]
    else:
        print(f'Start Playing: {assigned_sounds[button.pin]}')
        channels[button.pin] = sounds[button.pin].play()



MEDIA_PATH=os.environ.get('MEDIA_PATH','/home/pi/media')

if not os.path.exists(MEDIA_PATH):
    raise FileNotFoundError('Could not find media path file.')

files = glob.glob(os.path.join(MEDIA_PATH,"*.wav"))


startup = os.path.join(MEDIA_PATH,"startup","startup.wav")
print(f'playing: {startup}')
startup_sound = pygame.mixer.Sound(startup)
startup_sound.play()

gpio_pins = [2,3,4,17]
sounds = dict()
for file, gpi_pin in zip(files[0:4],gpio_pins):
    button = Button(gpi_pin)
    button.when_pressed = button_pressed
    sounds[button.pin] = pygame.mixer.Sound(file)
    assigned_sounds[button.pin] = file

print('Waiting')
pause()
