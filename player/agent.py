import json
import configparser
import time
from lib import(
    util
)
from res.settings import Inform
from audio import audio_transcriber
from audio import transcription
from gui.display import GUI
import PySimpleGUI as sg

class Agent:
    def __init__(self, inifile:configparser.ConfigParser) -> None:
       # init bariables
       self.inifile = inifile
       self.human_flag = True
       self.received = []   # holds orders from the server
       self.divined = []    # hold divine agents
       self.comments = []

       # game info setting
       self.alive = []  # hold alive player's name
       self.dead = [] # hold dead player's name
       self.gameContinue = True

       # load json format
       self.inform_info = Inform()
       self.inform_format = self.inform_info.get_Inform_format()

       # set transcriber
       self.transcriber = audio_transcriber.AudioTranscriber(inifile=self.inifile)
    
    def set_name(self, name:str) -> None:
        self.name = name
    
    def set_device_index(self, device_index:int) -> None:
        self.device_index = device_index
    
    def set_gui(self, gui:GUI, window:sg.Window) -> None:
         # set gui
         self.gui = gui
         self.window = window         

    def parse_info(self, receive:str) -> None:
        # parse information received from server

        received_list = receive.split("}\n{")

        for index in range(len(received_list)):
            received_list[index] = received_list[index].rstrip()

            if received_list[index][0] != "{":
                received_list[index] = "{" + received_list[index]

            if received_list[index][-1] != "}":
                received_list[index] += "}"

            self.received.append(received_list[index])
    
    def get_info(self) -> None:
        # stores information from server
        data = json.loads(self.received.pop(0))

        if data["gameInfo"] != None:
            self.gameInfo = data["gameInfo"]
        
        if data["gameSetting"] != None:
            self.gameSetting = data["gameSetting"]
        
        self.request = data["request"]
        self.talkHistory = data["talkHistory"]
        self.whisperHistory = data["whisperHistory"]
        self.human_message = data["humanMessage"]

        print("----get_info----")
        print(data)

    def daily_finish(self) -> None:
        pass
    
    def get_name(self) -> str:
        return self.name
    
    def talk(self) -> None:
        # talk time setting
        start_time = time.time()
        end_time = start_time + self.gameSetting["dailyTimeLimit"]
        self.transcriber.set_time_limit(time_limit=end_time)

        # start talk
        transcription.start(inifile=self.inifile, transcriber=self.transcriber, selected_device_index=self.device_index)

    def vote(self) -> str:

        self.window.write_event_value(key=self.gui.check_vote, value=(self.gameInfo["targetNameList"],self.human_message))
        self.window.write_event_value(key=self.gui.close_vote_window, value=None)

        while not self.gui.vote_flag:
            pass

        self.gui.vote_flag = False
        
        self.inform_info.reset_values()
        self.inform_info.update_message(message=self.gui.vote_targt)

        return self.convert_json()

    def whisper(self) -> None:
        pass

    def inform(self) -> None:
        self.window.write_event_value(key=self.gui.update_inform, value=self.human_message)
    
    def inform_check(self, image:str = None) -> str:
        self.window.write_event_value(key=self.gui.check_confirm, value=(self.human_message, image))

        while not self.gui.check_flag:
            pass

        message = self.gui.message
        self.gui.check_flag = False

        self.inform_info.reset_values()
        self.inform_info.update_message(message=message)

        return self.convert_json()
    
    def role_action(self) -> str:
        self.role = self.gameInfo["role"]

        self.window.write_event_value(key=self.gui.resize, value=(self.gui.role_path.format(role=self.role),
                                                                  self.gui.role_resize.format(role=self.role)))
        message = self.inform_check(image=self.gui.role_resize.format(role=self.role))

        self.window.write_event_value(key=self.gui.update_role, value=self.role)

        return message
    
    def base_info(self) -> str:
        self.inform_info.reset_values()
        self.inform_info.update_basic_info(name=self.name, human_flag=self.human_flag)
        return self.convert_json()

    def finish(self) -> str:
        self.gameContinue = False

    def convert_json(self) -> str:
        self.inform_info.update_inform_format()
        return json.dumps(self.inform_format,separators=(",",":"))
    
    def unique_action(self) -> str:
        self.window.write_event_value(key=self.gui.unique_action, value=(self.gameInfo["targetNameList"],self.human_message))
        self.window.write_event_value(key=self.gui.close_unique_window, value=None)

        while not self.gui.unique_action_flag:
            pass

        self.gui.unique_action_flag = False
        
        self.inform_info.reset_values()
        self.inform_info.update_message(message=self.gui.unique_target)

        return self.convert_json()

    def action(self) -> str:

        if self.request == "INITIALIZE":
            self.initialize()
        elif self.request == "NAME":
            return self.get_name()
        elif self.request == "ROLE":
            return self.role_action()
        elif self.request == "DAILY_FINISH":
            self.daily_finish()
        elif self.request == "TALK":
            self.talk()
        elif self.request == "VOTE":
            return self.vote()
        elif self.request == "WHISPER":
            self.whisper()
        elif self.request == "INFORM":
            self.inform()
        elif self.request == "INFORMCHECK":
            return self.inform_check()
        elif self.request == "BASEINFO":
            return self.base_info()
        elif self.request == "DIVINE":
            return self.unique_action()
        elif self.request == "DIVINELIE":
            return self.unique_action()
        elif self.request == "ATTACK":
            return self.unique_action()
        elif self.request == "PSYCHIC":
            return self.unique_action()
        elif self.request == "GUARD":
            return self.unique_action()
        elif self.request == "FINISH":
            self.finish()
        
        return ""