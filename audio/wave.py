import configparser
import pyaudio
import json
import numpy
from res import settings

class Wave:
    def __init__(self, inifile:configparser.ConfigParser) -> None:
            self.audio = pyaudio.PyAudio()
            self.channels = inifile.getint("audio","channels")
            self.width = self.audio.get_sample_size(format=settings.format)
            self.rate = inifile.getint("audio","rate")
    
    def convert_json(self, audio:numpy.ndarray) -> str:
          data = dict(channels=self.channels, width=self.width, rate=self.rate, audio=audio.tolist())

          print(data)

          result = json.dumps(data)
          
          return result