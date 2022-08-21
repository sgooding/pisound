
import os
import glob
from pydub import AudioSegment

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