import concurrent.futures
from lib import (
    util,
    client
)
util.last_resort()
from player.agent import Agent
import PySimpleGUI as sg
from gui import display
import os

def listen_gui(gui:display.GUI):
    gui.open_window()
    gui.resize()

    while True:
        event, values = gui.read()

        if event in ((sg.WIN_CLOSED, 'Exit')):
            break
        elif event == gui.hide_button:
            gui.hide_role()
    
    gui.close_window()

def main():
    config_path = "./res/config.ini"
    inifile = util.check_config(config_path=config_path)
    inifile.read(config_path,"utf-8")

    gui = display.GUI(inifile=inifile)

    # multi process
    executor = concurrent.futures.ThreadPoolExecutor()
    future = executor.submit(listen_gui, gui)

    name = input("あなたの名前を入力してください！:")
    
    agent = Agent(inifile=inifile,gui=gui,name=name)

    print("connecting to server...")
    connection = client.Client(config_path=config_path)
    connection.connect()

    agent.transcriber.set_connection(connection=connection)

    while agent.gameContinue:

        if len(agent.received) == 0:
            agent.parse_info(receive=connection.receive())
        
        agent.get_info()
        message = agent.action()

        if message != "":
            connection.send(message=message)
    
    gui.close_window()
    connection.close()

if __name__ == "__main__":
    main()