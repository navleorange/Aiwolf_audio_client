import configparser
import webrtcvad

class VadWrapper:
    def __init__(self, inifile:configparser.ConfigParser):
        self.vad = webrtcvad.Vad(inifile.getint("audio","vad_mode"))
        self.RATE = inifile.getint("audio","rate")
        self.SILENT_CHUNKS_THRESHOLD = inifile.getint("audio","silent_chunks_threshold")

    def is_speech(self, in_data):
        return self.vad.is_speech(in_data, self.RATE)
