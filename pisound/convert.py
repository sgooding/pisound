
import os
import glob
import time
import shutil
from pydub import AudioSegment
import pygame


def play_loading_sound(loading_wav_file):
    print(f'playing: {loading_wav_file}')
    loading_sound = pygame.mixer.Sound(loading_wav_file)
    loading_sound.play()

def automount_usb():
    if not os.path.exists('/dev/sda1'):
        print('No USB Drive')
        return
    
    print('trying to mount /dev/sda1')
    os.system('sudo mount -t vfat /dev/sda1 /mnt/usb0')
    time.sleep(1)

    basedir = os.environ.get('MEDIA_PATH','/home/pi/media')
    print('verify any mp3 files exist')
    files = glob.glob('/mnt/usb0/*.mp3')

    if len(files) == 0:
        print(f'No files found.')
        return

    print(f'Found The Following Files: {files}')

    if len(files) != 4:
        print(f'EXACTLY 4 files must exist on the usb drive, not {len(files)}.')
        return
    
    original_files = glob.glob(os.path.join(basedir,'*.mp3'))

    original_basenames = [os.path.basename(i) for i in original_files]
    new_basenames = [os.path.basename(i) for i in files]

    set_dif = set(original_basenames).symmetric_difference(set(new_basenames))
    if len(set_dif) == 0:
        print('mp3 files are the same, returning early')
        return

    original_files += glob.glob(os.path.join(basedir,'*.wav'))


    print(f'Removing the following files from {original_files}')

    elevator = glob.glob('/home/pi/media/startup/elevator*')
    pygame.mixer.music.load(elevator[0])
    pygame.mixer.music.play()
    for original_file in original_files:
        if os.path.exists(original_file):
            print(f'Removing: {original_file}')
            os.remove(original_file)

    for file in files:
        print(f'Copy {file} to {basedir}')
        shutil.copy(file,basedir)
        
    print(f'Completed USB Copy')

    os.system('sudo umount /mnt/usb0')

def convert_file(filename):
    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(filename)
    wav_path = os.path.join(os.path.split(filename)[0],
                            os.path.splitext(filename)[0]+".wav")
    sound.export(wav_path, format="wav")

def convert():

    converting = False
    basedir = os.environ.get('MEDIA_PATH','/home/pi/media')

    files = glob.glob(os.path.join(basedir,'*.mp3'))
    for file in files:

        mp3_basename = os.path.splitext(os.path.basename(file))[0]
        wav_path = os.path.join(basedir,mp3_basename+'.wav')
        if os.path.exists(wav_path):
            print(f'Found: {wav_path}')
            continue

        print(f'Converting: {file} into {wav_path}')
        converting = True

        # convert wav to mp3                                                            
        sound = AudioSegment.from_mp3(file)
        sound.export(wav_path, format="wav")

    pygame.mixer.music.stop()

    if converting:
        tada = glob.glob('/home/pi/media/startup/tada*')
        pygame.mixer.music.load(tada[0])
        pygame.mixer.music.play()

if __name__ == '__main__':
    convert()