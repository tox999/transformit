from posixpath import split
import pprint
from typing import Any, Tuple
from urllib.parse import urlparse
import requests
import json


# config
# https://www.dnd5eapi.co/docs/#get-/api/-endpoint-
SECRETS_FILE_PATH = "./secrets.json"
DND5_API_HOST = "https://www.dnd5eapi.co/"
COMMANDS ={
    "exit" : 
    {
        "func": close_app, 
        "alt_names": ["q","quit","exit","close"]
    },
    "hi" : 
    {
        "func": hi, 
        "alt_names": ["h","hey","hello"]
    },
}

def hi(*args, **kwargs)-> Tuple(str, bool):
    return "hi", False

def close_app(*args, **kwargs) -> Tuple(str, bool):
    return "bye", True

def get_secrets() -> dict:
    with open(SECRETS_FILE_PATH) as f:
        secrets = json.load(f)
        return secrets
    
def send_request(url, ep):
    headers={}
    url = urlparse.urljoin(url, ep)
    response = requests.request("GET", url, headers=headers)
    print(response.text)

def parse_user_cmd(user_cmd:str)->Tuple(str,Any,Any):
    user_cmd.split(" ")
    raise NotImplemented


def main(*args, **kwargs):
    url = kwargs["url"]
    should_close = False
    while(should_close == False):
        user_cmd = input()
        
        cmd_name, args, kwargs = parse_user_cmd(user_cmd)
      
        alt_cmd_names = {item for sublist in [v["alt_names"] for _,v in COMMANDS.items()] for item in sublist}
        cmd_names = COMMANDS.keys().union(alt_cmd_names)  
        if cmd_name not in cmd_names:
            pprint(f"commands does not exists. Possible commands: {cmd_names}")
            continue
        
        for cmd_lib_name, cmd_details in COMMANDS.items():
            if cmd_name != cmd_lib_name:
                if cmd_name in cmd_details["alt_names"]:
                    cmd = cmd_lib_name
            else:
                cmd = cmd_name

        response, should_close = COMMANDS[cmd](*args, **kwargs)
        pprint(response)


if __name__ == "__main__":
    main(secrets=get_secrets(),url=DND5_API_HOST)

