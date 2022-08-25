from distutils.core import setup
from pisound import __version__
setup(name='pisound',
      version=__version__,
      description='Raspberry pi sound board',
      author='Sean Gooding',
      author_email='sgooding@gmail.com',
      url='https://github.com/sgooding/pisound',
      packages=['pisound'],
      install_requires=['pydub==0.24.1',
                        'gpiozero==1.6.2'
                       ]
     )
