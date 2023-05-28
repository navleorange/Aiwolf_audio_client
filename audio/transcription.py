import configparser

from . import audio_transcriber
from . import audio_utils

def transcription(inifile:configparser.ConfigParser) -> None:
    transcriber = audio_transcriber.AudioTranscriber(inifile=inifile)

    valid_devices = audio_utils.get_valid_input_devices()
    print("使用可能なオーディオデバイス:")
    audio_utils.display_valid_input_devices(valid_devices=valid_devices)

    # 対象のDeviceIndexを入力
    selected_device_index = int(input("対象のDeviceIndexを入力してください: "))

    # 文字起こしを開始
    transcriber.start_transcription(selected_device_index=selected_device_index, inifile=inifile)
