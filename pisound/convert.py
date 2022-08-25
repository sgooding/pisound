
import os
import glob
import time
import shutil
from pydub import AudioSegment

def automount_usb():
    if not os.path.exists('/dev/sda1'):
        print('No USB Drive')
        return
    
    print('trying to mount /dev/sda1')
    os.system('sudo mount -t vfat /dev/sda1 /mnt/usb0 -o umask=000')
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
    original_files += glob.glob(os.path.join(basedir,'*.wav'))
    print(f'Removing the following files from {original_files}')

    for original_file in original_files:
        if os.path.exists(original_file):
            print(f'Removing: {original_file}')
            os.remove(original_file)

    for file in files:
        print(f'Copy {file} to {basedir}')
        shutil.copy(file,basedir)
        
    print(f'Completed USB Copy')

    os.system('sudo umount /mnt/usb0')

def convert():

    basedir = os.environ.get('MEDIA_PATH','/home/pi/media')

    files = glob.glob(os.path.join(basedir,'*.mp3'))
    for file in files:

        mp3_basename = os.path.splitext(os.path.basename(file))[0]
        wav_path = os.path.join(basedir,mp3_basename+'.wav')
        if os.path.exists(wav_path):
            print(f'Found: {wav_path}')
            continue

        print(f'Converting: {file} into {wav_path}')

        # convert wav to mp3                                                            
        sound = AudioSegment.from_mp3(file)
        sound.export(wav_path, format="wav")

if __name__ == '__main__':
    convert()