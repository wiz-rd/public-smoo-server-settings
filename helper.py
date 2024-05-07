import os
import re
import sys
import json
import socket
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

# Leaving this to tell the keys and values
# of the ban files. Consider this like a default
# or template for readability.
BAN_FILE_STRUCTURE = {
    "BanList": {
        "Enabled": True,
        "Players": [
            "00000001-0000-0000-0000-000000000000"
        ],
        "IpAddresses": [],
        "Stages": []
    }
}

OPTIONS_FILENAME = "ban_options.json"
BAN_FILENAME = "bans.json"

class APIHandler():
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

        try:
            self.port = int(port)
        except ValueError:
            sys.exit(f"The port provided, {port}, is not an integer and cannot be converted to one.")

        if api_token == "":
            raise ValueError("BanHandler API token cannot be empty string.")

        self.api_token = api_token

    def __str__(self) -> str:
        return f"host: {self.host}, port: {self.port}, api_token: {self.api_token}"

    def command(self, command: str, *arguments: str):
        """
        Overall
        -------
        Makes an API request to the server
        with the command provided.

        Accepts
        -------
        - command - the command to be sent (e.g. ban, loadsettings, sendall, etc)
        - arguments - everything after the command, so in "ban player Tyrant8080" it would be "player Tyrant8080"

        Returns
        -------
        The response from the server.
        """
        if len(arguments) == 0: args = ""
        if len(arguments) > 1: args = " ".join(arguments)
        else: args = arguments[0]


        server_request = {
            "API_JSON_REQUEST": {
                "Token": self.api_token,
                "Type": "Command",
                "Data": f"{command} {args}",
                # sending the request
            }
        }

        # if no arguments were provided, assume it's just a single word
        # such as loadsettings or something
        if args == "": server_request["API_JSON_REQUEST"]["Data"] = command

        print(f"Sending '{command}' with args '{args}' to server")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            server.connect((self.host, self.port))
            server.send(json.dumps(server_request).encode())
            response = server.recv(4096)
            server.close()
            return response.decode()
        except ConnectionRefusedError:
            print("The server appears to be offline or does not accept JSON API requests. Exiting program.")
            sys.exit()

    def valid_profile(self, ID: str) -> bool:
        """
        Overall
        -------
        Returns a boolean indicating whether or not the profile ID provided is
        a valid Switch account ID via Regex.

        Accepts
        -------
        - ID - the id to validate.

        Returns
        -------
        A True/False of whether or not the ID is valid.
        """
        regex = "^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$"
        
        # if a match is found, match_found is true because re.match() returns something
        match_found = re.match(regex, ID) is not None
        return match_found

    def ban(self, method: Literal["profile", "player", "ip"] = "profile", argument: str = ""):
        """
        Overall
        -------
        Makes an API request that
        bans the profile/ip provided.

        Accepts
        -------
        - method - the way you will ban the player (by profile - such as Ryujinx or Switch profile,
        by IP address, or by player name)
        - argument - the player/profile to be banned. Cannot be empty.

        Returns
        -------
        The response from the server.
        """
        if argument == "":
            raise ValueError("'argument' arg for ban() cannot be an empty string.")

        # if the profile is not valid AND the method is profile
        if not self.valid_profile(argument) and method == "profile":
            raise ValueError("The provided profile is invalid.")

        return self.command("ban", method, argument)

    def unban(self, method: Literal["profile", "ip"] = "profile", argument: str = ""):
        """
        Overall
        -------
        Makes an API request that
        unbans the profile/ip provided. Identical to ban() in pretty much every way aside from
        the exact command sent to the server.

        Accepts
        -------
        - method - the way you will unban the player (by profile - such as Ryujinx or Switch profile -
        by IP address)
        - argument - the player/profile to be banned. Cannot be empty.
        - NOTE: this version does not accept player names as player names are not stored.
        You will have to know the profile ID to be able to unban specific players.

        Returns
        -------
        The response from the server.
        """
        if argument == "":
            raise ValueError("'argument' arg for unban() cannot be an empty string.")

        # if the profile is not valid AND the method is profile
        if not self.valid_profile(argument) and method == "profile":
            raise ValueError("The provided profile is invalid.")

        return self.command("unban", method, argument)


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
    E.g., gets "bans.json".

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


def compare_and_update_bans(repo_url: str) -> dict | None:
    """
    Overall
    -------
    Compares the local ban info to the hosted file and updates the local
    file accordingly. Does NOT unban individuals removed. This is intentional.

    Accepts
    -------
    - repo_url - the repo where the file to be compared with is stored.

    Returns
    -------
    A dictionary or None; whether or not there was a difference. If so, the
    server will need to be updated.
    """
    local_file_data = load_local_file(BAN_FILENAME)
    repo_file_data = load_repository_file(repo_file_url=repo_url + "bans.json")

    if local_file_data != repo_file_data:
        print("Some bans are different... updating the local file!")
        local_file_data = repo_file_data
        update_local_file(BAN_FILENAME, local_file_data)
        """
        This should return something like the following:

        "BanList": {
            "Enabled": True,
            "Players": [],
            "IpAddresses": [],
            "Stages": []
        }

        See top of this file for the whole structure of bans.json.
        """
        return local_file_data["BanList"]
    else:
        return None
