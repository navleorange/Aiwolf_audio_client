import configparser
from . import audio_utils

def search_device() -> None:

    valid_devices = audio_utils.get_valid_input_devices()

    message = "使用可能なオーディオデバイス:\n"
    message += audio_utils.display_valid_input_devices(valid_devices=valid_devices)
    message += "対象のDeviceIndexを入力してください: "

    return message, len(valid_devices)

def start(inifile:configparser.ConfigParser, transcriber, selected_device_index) -> None:
    # 文字起こしを開始
    transcriber.start_transcription(selected_device_index=selected_device_index, inifile=inifile)