import configparser

from . import audio_transcriber
from . import audio_utils
from gui.display import GUI

def search_device(inifile:configparser.ConfigParser, gui:GUI) -> None:
    transcriber = audio_transcriber.AudioTranscriber(inifile=inifile, gui=gui)

    valid_devices = audio_utils.get_valid_input_devices()
    print("使用可能なオーディオデバイス:")
    audio_utils.display_valid_input_devices(valid_devices=valid_devices)

    # 対象のDeviceIndexを入力
    selected_device_index = int(input("対象のDeviceIndexを入力してください: "))

    return (transcriber, selected_device_index)

def start(inifile:configparser.ConfigParser, transcriber, selected_device_index) -> None:
    # 文字起こしを開始
    transcriber.start_transcription(selected_device_index=selected_device_index, inifile=inifile)
