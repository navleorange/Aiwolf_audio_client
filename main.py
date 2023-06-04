from lib import (
    util,
    client
)
util.last_resort()
from player.agent import Agent

def main():
    config_path = "./res/config.ini"
    inifile = util.check_config(config_path=config_path)
    inifile.read(config_path,"utf-8")

    name = input("あなたの名前を入力してください！:")
    agent = Agent(inifile=inifile, name=name)

    print("connecting to server...")
    connection = client.Client(config_path=config_path)
    connection.connect()

    #agent.transcriber.set_connection(connection=connection)

    while agent.gameContinue:

        if len(agent.received) == 0:
            agent.parse_info(receive=connection.receive())
        
        agent.get_info()
        message = agent.action()

        if message != "":
            connection.send(message=message)
    
    connection.close()

if __name__ == "__main__":
    main()