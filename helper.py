import os
import sys
import json
from typing import Literal
from json import JSONDecodeError
import requests

DEFAULT_JSON = {
    "//comment": "The repo can be any raw file. This is the default that bans will be synced with.",
    "repo_url": "https://raw.githubusercontent.com/wiz-rd/public-smoo-server-settings/main/",
    "//comment2": "The rest is related to the server and its API.",
    "token": "SETTHISTOYOURSERVERTOKEN, see https://github.com/Istador/SmoOnlineServer/blob/json-api/Server/JsonApi/README.md for help",
    "host": "localhost",
    "port": "1027",
}

OPTIONS_FILENAME = "ban_options.json"
BAN_FILENAME = "bans.json"

class BanHandler():
    """
    Overall
    -------
    Handles banning, super neato.
    """
    def __init__(self, host: str = "localhost", port: int = 1027, api_token: str = "") -> None:
        """
        Overall
        -------
        Handles bans. Run obj.ban("profile", <profile>)
        or obj.ban("ip", <ip>) to ban users. This will be used
        to ban stuff dynamically.
        """
        self.host = host
        self.port = port

        if api_token == "":
            raise ValueError("BanHandler API token cannot be empty string.")

        self.api_token = api_token

    def ban(self, method: Literal["profile", "ip"] = "profile", argument: str = ""):
        """
        Overall
        -------
        Makes an API request that
        bans the profile/ip provided.

        Returns
        -------
        The response from the server.
        """
        ban_request = {
            "API_JSON_REQUEST": {
                "Token": self.api_token,
                "Type": "Command",
                "Data": f"ban {method} {argument}",
                # banning the profile or ip
            }
        }

        response = requests.Request(f"{self.host}:{self.port}", json.dumps(ban_request))
        return response.data

    def unban(self, method: Literal["profile", "ip"] = "profile", argument: str = ""):
        """
        Overall
        -------
        Makes an API request that
        unbans the profile/ip provided. Identical to ban() in pretty much every way aside from
        the exact command sent to the server.

        Returns
        -------
        The response from the server.
        """
        ban_request = {
            "API_JSON_REQUEST": {
                "Token": self.api_token,
                "Type": "Command",
                "Data": f"unban {method} {argument}",
                # unbanning the profile or ip
            }
        }

        response = requests.Request(f"{self.host}:{self.port}", json.dumps(ban_request))
        return response.data


def prepare_options_file() -> dict:
    """
    Overall
    -------
    Makes the default "options.json" file if it does not exist already.

    Returns
    -------
    - dict (the options)
    """

    if os.path.exists(OPTIONS_FILENAME):
        with open(OPTIONS_FILENAME, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except JSONDecodeError:
                print("The JSON file was formatted incorrectly. Please correct it or delete the file and let it be remade.")
                sys.exit("Repair or remove options.json")
    else:
        open(OPTIONS_FILENAME, "w+", encoding="utf-8").close()
        print("The options.json does not exist. Making it now.")
        with open(OPTIONS_FILENAME, "r+", encoding="utf-8") as f:
            f.write(json.dumps(DEFAULT_JSON, indent=4))
        return DEFAULT_JSON


def setup() -> dict:
    """
    Overall
    -------
    Performs first-time setup, like making files if they don't exist etc.

    Returns
    -------
    dict (of options.json)
    """
    options = prepare_options_file()
    # space for additional methods here. Redundant otherwise

    return options


def load_local_file(filepath: str) -> dict:
    """
    Overall
    -------
    Grabs the current item.

    E.g., gets "bans.json" if selected.
    Or "public_settings.json" if desired.

    Accepts
    -------
    - filepath - The path of the file to be read in.

    Returns
    -------
    A JSON object of the contents of "filepath".
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_repository_file(repo_file_url: str) -> dict:
    """
    Overall
    -------
    Grabs the item from the given github repo and returns
    it as a json object.

    Accepts
    -------
    - repo_file_url - The URL of the static file to be compared to.

    Returns
    -------
    A JSON object of the text of the response from github_file_url
    """
    response = requests.get(repo_file_url, timeout=100)
    return json.loads(response.text)

def update_local_file(filename: str, contents: dict) -> None:
    """
    Overall
    -------
    Replaces the contents of the file with the updated contents, presumably from GitHub.

    Accepts
    -------
    - filename - the name of the file
    - contents - the contents of the file in question

    Returns
    -------
    ABSOLUTELY NOTHING >:D
    Nahh there's just nothing to return pfff.
    """
    # ...well this function was a lot shorter than I thought
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(contents, indent=4))

def compare_and_update(repo_url: str) -> dict | None:
    """
    Overall
    -------
    Compares the local ban info to the hosted file and updates the local
    file accordingly.

    Accepts
    -------
    - repo_url - the repo where the file to be compared with is stored.

    Returns
    -------
    A dictionary or None; whether or not there was a difference. If so, the
    server will need to be updated.
    """
    local_file_data = load_local_file(BAN_FILENAME)
    repo_file_data = load_repository_file(repo_file_url=repo_url)

    if local_file_data != repo_file_data:
        print("Some bans are different... updating the local file!")
        local_file_data = repo_file_data
        update_local_file(OPTIONS_FILENAME, local_file_data)
        return local_file_data
    else:
        print("Your bans are up to date!")
        return None
