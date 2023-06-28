import time
import asyncio
import queue
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pyaudio
import configparser

from . import (
    audio_utils,
    vad_utils,
    wave
)

import json
from res.settings import Inform
import PySimpleGUI as sg
from gui.display import GUI

class AudioTranscriber:
    def __init__(self, inifile:configparser.ConfigParser):
        self.inifile = inifile
        self.vad_wrapper = vad_utils.VadWrapper(inifile=self.inifile)
        self.wave = wave.Wave(inifile=self.inifile)
        self.silent_chunks = 0  # just count silent variable
        self.speech_buffer = []
        self.audio_queue = queue.Queue()
        self.inform_info = Inform()
        self.inform_format = self.inform_info.get_Inform_format()
        self.whisper_use = self.inifile.getboolean("whisper","use_flag")

    def set_gui(self, gui:GUI, window:sg.Window) -> None:
        self.gui = gui
        self.window = window

    def set_connection(self, connection) -> None:
        self.connection = connection
    
    def set_model_wrapper(self, model) -> None:
        self.model_wrapper = model

    def set_time_limit(self, time_limit) -> None:
        self.time_limit = time_limit

    def send_audio(self, audio_data_np) -> None:
        self.inform_info.reset_values()
        self.inform_info.update_audio(audio=self.wave.get_audio_dict(audio=audio_data_np))
        self.inform_info.update_request(request=self.inform_info.request_class.convert_audio)
        self.inform_info.update_inform_format()

        if time.time() >= self.time_limit:
            self.inform_info.reset_values()
            return

        self.connection.send(message=json.dumps(self.inform_format,separators=(",",":")))

    def listen_text(self) -> None:
        time_out = self.time_limit - time.time()

        print("listen timeout:" + str(time_out))

        if time_out > 0:
            self.connection.set_time_out = time_out
        else:
            return

        segments = self.connection.receive()

        if segments != None:
            segments = json.loads(segments)
            self.window.write_event_value(key=self.gui.update_comments, value=segments["humanMessage"])

    async def transcribe_audio(self) -> None:
        with ThreadPoolExecutor() as executor:

            while time.time() < self.time_limit:

                if self.whisper_use:
                    audio_data_np = await asyncio.get_event_loop().run_in_executor(
                        executor, self.audio_queue.get
                    )
                    segments = await asyncio.get_event_loop().run_in_executor(
                        executor, self.model_wrapper.transcribe, audio_data_np
                    )

                    for segment in segments:
                        print(segment.text)
                else:
                    audio_data_np = await asyncio.get_event_loop().run_in_executor(
                        executor, self.audio_queue.get
                    )
                    
                    # send to server
                    await asyncio.get_event_loop().run_in_executor(
                        executor, self.send_audio, audio_data_np
                    )

                    # receive from server
                    await asyncio.get_event_loop().run_in_executor(
                        executor, self.listen_text
                    )

        self.connection.restore_time_out()

    def process_audio(self, in_data, frame_count, time_info, status):
        is_speech = self.vad_wrapper.is_speech(in_data)

        if is_speech:
            self.silent_chunks = 0
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            self.speech_buffer.append(audio_data)
        else:
            self.silent_chunks += 1

        if (
            not is_speech
            and self.silent_chunks > self.vad_wrapper.SILENT_CHUNKS_THRESHOLD
        ):
            if len(self.speech_buffer) > self.inifile.getint("audio","speech_thareshold"):
                audio_data_np = np.concatenate(self.speech_buffer)
                self.speech_buffer.clear()
                self.audio_queue.put(audio_data_np)
            else:
                # noise clear
                self.speech_buffer.clear()

        return (in_data, pyaudio.paContinue)

    def start_transcription(self, selected_device_index:int, inifile:configparser.ConfigParser) -> None:
        stream = audio_utils.create_audio_stream(inifile=inifile, selected_device_index=selected_device_index, callback=self.process_audio)
        
        self.window.write_event_value(key=self.gui.update_inform, value="話し合いを始めてください")
        asyncio.run(self.transcribe_audio())
        stream.start_stream()
        stream.stop_stream()
        stream.close()
