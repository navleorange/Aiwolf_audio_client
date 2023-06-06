import os
import sys
import errno
import configparser
import random
import datetime
import time
import glob

def read_text(path:str):
    with open(path,"r",encoding="utf-8") as f:
        return f.read().splitlines()

def random_seed() -> None:
     # 乱数の設定
    now = datetime.datetime.now()
    random.seed(int(time.mktime(now.timetuple())))

def random_select(data:list):
    return random.choice(data)

def is_json_complate(responces:bytes) -> bool:

    try:
        responces = responces.decode("utf-8")
    except:
        return False
    
    if responces == "":
        return False

    cnt = 0

    for word in responces:
        if word == "{":
            cnt += 1
        elif word == "}":
            cnt -= 1
    
    return cnt == 0

def check_config(config_path:str) -> configparser.ConfigParser:

    if not os.path.exists(config_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)
    
    return configparser.ConfigParser()

def last_resort() -> None:
    # venvのpathが通ったり通らなかったり気まぐれなので...
    cwd = os.getcwd()
    env_path = cwd + "\\venv\\Lib\\site-packages"

    if not env_path in sys.path:
        sys.path.append(env_path)

def select_unidentified(unidentified_path:str):
    unidentified_images = glob.glob(unidentified_path)
    return random_select(unidentified_images)