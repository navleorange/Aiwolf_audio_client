from lib import util
util.last_resort()
from audio import transcription

def main():
    config_path = "./res/config.ini"
    inifile = util.check_config(config_path=config_path)
    inifile.read(config_path,"utf-8")

    transcription.transcription(inifile=inifile)

if __name__ == "__main__":
    main()