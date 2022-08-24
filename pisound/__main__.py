import pygame
import glob
import os

from gpiozero import Button
from signal import pause
import time

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
    global assigned_sounds
    print(f'pressed: {button.pin}')

    if button.pin in channels:
        print(f'Stop Playing: {assigned_sounds[button.pin]}')
        channels[button.pin].stop()
        del channels[button.pin]
        print(f'Removed: {assigned_sounds[button.pin]}')
    else:
        print(f'Create Sound and playing: {assigned_sounds[button.pin]}')
        channels[button.pin] = sounds[button.pin].play()

def shutdown_pi():
    global assigned_sounds
    print('Good Bye')
    shutdown = os.path.join(MEDIA_PATH,"startup","shutdown.wav")
    print(f'playing: {shutdown}')
    for channel in channels.values():
        channel.stop()
    
    shutdown_sound = pygame.mixer.Sound(shutdown)
    shutdown_sound.play()
    time.sleep(15)
    os.system('sudo shutdown -h now')




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
    button = Button(gpi_pin, pull_up=True, hold_time=4)
    button.when_pressed = button_pressed
    button.when_held = shutdown_pi
    sounds[button.pin] = pygame.mixer.Sound(file)
    assigned_sounds[button.pin] = file


print('Waiting')
pause()
