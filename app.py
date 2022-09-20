from posixpath import split
from pprint import pprint
from typing import Any, Tuple
from urllib.parse import urlparse
import requests
import json

# change 3
# change 2
# change 1
# Config
# https://www.dnd5eapi.co/docs/#get-/api/-endpoint-
SECRETS_FILE_PATH = "./secrets.json"
DND5_API_HOST = "https://www.dnd5eapi.co/"
COMMANDS ={
    "exit" : 
    {
        "func": "close_app", 
        "alt_names": ["q","quit","exit","close"]
    },
    "hi" : 
    {
        "func": "hi", 
        "alt_names": ["h","hey","hello"]
    },
}

class Engine:
    def hi(*args, **kwargs)-> Tuple[str, bool]:
        return "hi", False

    def close_app(*args, **kwargs) -> Tuple[str, bool]:
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

def parse_user_cmd(user_cmd:str, cmd_arg_sep=" ", arg_sep=" ", kwargs_sep="=")->Tuple[str,Any,Any]:
    cmd_and_args = user_cmd.split(cmd_arg_sep)
    args=[]
    kwargs=dict()
    cmd_name = cmd_and_args[0]

    if len(cmd_and_args) > 1:
        args_and_kwargs = cmd_and_args[1:].split(arg_sep)
        args = [arg for arg in args_and_kwargs if kwargs_sep not in arg]
        
        for kwarg in args_and_kwargs:
            if kwargs_sep in kwarg:
                kwarg_name_and_value = kwarg.split(kwargs_sep)
                kwarg_name = kwarg_name_and_value[0]
                kwarg_value = None
                if len(kwarg_name_and_value) > 1:
                    kwarg_value = kwarg_name_and_value[1:]
                kwargs[kwarg_name] = kwarg_value
    
    return cmd_name, args, kwargs


def main(*args, **kwargs):
    url = kwargs["url"]
    engine = Engine()
    should_close = False

    while(should_close == False):
        user_cmd = input("Your command?")
        
        cmd_name, args, kwargs = parse_user_cmd(user_cmd)
      
        alt_cmd_names = {item for sublist in [v["alt_names"] for _,v in COMMANDS.items()] for item in sublist}
        cmd_names = set(COMMANDS.keys()).union(alt_cmd_names)  
        if cmd_name not in cmd_names:
            pprint(f"Commands does not exist. Possible commands: {cmd_names}")
            continue
        
        for cmd_lib_name, cmd_details in COMMANDS.items():
            if cmd_name != cmd_lib_name:
                if cmd_name in cmd_details["alt_names"]:
                    cmd = cmd_lib_name
            else:
                cmd = cmd_name
        try:
            cmd_func = getattr(engine, cmd)
            response, should_close = cmd_func(*args, **kwargs)
        except AttributeError:
            response = "Cannot execute - not implemented."
        
        pprint(response)


if __name__ == "__main__":
    main(secrets=get_secrets(),url=DND5_API_HOST)

