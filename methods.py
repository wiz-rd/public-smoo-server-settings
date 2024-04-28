import json
import sys

DEFAULT_JSON = {
    "use_bans": True,
    "use_default_server_settings": False,
    "repo_url": "https://raw.githubusercontent.com/wiz-rd/public-smoo-server-settings/main/",
    "token": "SETTHISTOYOURSERVERTOKEN, see https://github.com/Istador/SmoOnlineServer/blob/json-api/Server/JsonApi/README.md for help",
    "host": "localhost",
    "port": "1027",
}


def make_file_if_necessary(filename: str):
    """
    Makes the default "options.json" file if it does not exist already.
    """
    try:
        open(filename, "x").close()
        print("The options.json does not exist. Making it now.")
        with open(filename, "r+") as f:
            f.write(json.dumps(DEFAULT_JSON))

    except FileExistsError:
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except:
                print("The JSON file was formatted incorrectly. Please ensure it's correct or delete it and let it be remade.")


def setup(kill_if_format_err: bool):
    """
    Performs first-time setup of the script.
    """
    options = make_file_if_necessary("options.json")
    
    if options is not None:
        return options
    elif kill_if_format_err:
        sys.exit()
    else:
        # use the default options if the JSON is formatted incorrectly
        return DEFAULT_JSON