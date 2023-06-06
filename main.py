import concurrent.futures
from lib import (
    util,
    client
)
util.last_resort()
from player.agent import Agent
import PySimpleGUI as sg
from gui import display
from audio import whisper_utils
import time

def execute_werewolf(agent:Agent, config_path:str):

    # inform 
    agent.window.write_event_value(key=agent.gui.update_inform, value="connecting to server...\n")


    connection = client.Client(config_path=config_path)
    connection.connect()

    agent.transcriber.set_connection(connection=connection)

    while agent.gameContinue:

        if len(agent.received) == 0:
            agent.parse_info(receive=connection.receive())
        
        agent.get_info()
        message = agent.action()

        if message != "":
            print("send:")
            print(message)
            connection.send(message=message)
    
    connection.close()
    agent.window.write_event_value(key=agent.gui.finish, value=None)

def main():
    config_path = "./res/config.ini"
    inifile = util.check_config(config_path=config_path)
    inifile.read(config_path,"utf-8")
    whisper_flag = inifile.getboolean("whisper","use_flag")

    # init agent
    agent = Agent(inifile=inifile)

    if whisper_flag:
        model_wrapper = whisper_utils.WhisperModelWrapper(inifile=inifile)
        agent.transcriber.set_model_wrapper(model=model_wrapper)

     # init gui
    gui = display.GUI(inifile=inifile)
    gui.open_window()

    # get agent information from gui
    agent.set_gui(gui=gui, window=gui.window)
    agent.set_name(name=gui.get_name())
    agent.set_device_index(device_index=gui.get_audio_index())
    agent.transcriber.set_gui(gui=gui, window=gui.window)

    # multi thread
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    future = executor.submit(execute_werewolf, agent, config_path)

    # gui loop
    while True:
        event, values = gui.read()

        if event in ((sg.WIN_CLOSED, 'Exit')):
            break
        elif event == gui.hide_button:
            gui.hide_role()
        elif event == gui.get_name:
            gui.get_name()
        elif event == gui.update_comments:
            gui.update_comments(comment=values[event])
        elif event == gui.update_inform:
            gui.update_inform(message=values[event])
        elif event == gui.check_confirm:
            gui.check_confirm(message=values[event][0], image=values[event][1])
        elif event == gui.resize:
            gui.resize(image_path=values[event][0], save_path=values[event][1])
        elif event == gui.update_role:
            gui.update_role(role=values[event])
        elif event == gui.check_vote:
            gui.check_vote(vote_list=values[event])
        elif event == gui.close_vote_window:
            gui.close_vote_window()
        elif future != None:
            print(future.result())

if __name__ == "__main__":
    main()