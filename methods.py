import json
import sys
import requests
from urllib import request

DEFAULT_JSON = {
    "//comment": 'set any of the items in "use" to false if you do not want to update them with the chosen repo.',
    "use": {
        # if they want to use the bans file
        "bans.json": True,
    },
    "//comment2": 'The repo can be any raw file.',
    "repo_url": "https://raw.githubusercontent.com/wiz-rd/public-smoo-server-settings/main/",
    "//comment3": 'The rest is related to the server and its API.',
    "token": "SETTHISTOYOURSERVERTOKEN, see https://github.com/Istador/SmoOnlineServer/blob/json-api/Server/JsonApi/README.md for help",
    "host": "localhost",
    "port": "1027",
}


def make_file_if_necessary(filename: str):
    """
    Overall
    -------
    Makes the default "options.json" file if it does not exist already.

    Returns
    -------
    - dict (the options)
    - None (if options.json is formatted incorrectly)
    

    """
    try:
        open(filename, "x").close()
        print("The options.json does not exist. Making it now.")
        with open(filename, "r+") as f:
            f.write(json.dumps(DEFAULT_JSON, indent=4))

    except FileExistsError:
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except:
                print("The JSON file was formatted incorrectly. Please ensure it's correct or delete it and let it be remade.")
                return None


def setup(kill_if_format_err: bool):
    """
    Overall
    -------
    Performs first-time setup of the script.

    Returns
    -------
    - dict (the custom options.json)
    - dict (the default options, if options.json does not exist)
    - EXITS the program entirely
    """
    options = make_file_if_necessary("options.json")
    
    # if the options file exists
    # OR if the file isn't to be killed
    # send the custom options or the default options,
    # whichever "options" equals
    if options != DEFAULT_JSON or options == DEFAULT_JSON:
        return options
    elif kill_if_format_err and options is None:
        print("Files are formatted incorrectly, exiting")
        sys.exit()
    else:
        return DEFAULT_JSON


def get_option_items(filepath: str):
    """
    Overall
    -------
    Grabs the current item.

    E.g., gets "bans.json" if selected.
    Or "public_settings.json" if desired.

    Returns
    -------
    A JSON object of the contents of "filepath".
    """
    with open(filepath, "r") as f:
        return json.load(f)


def get_github_items(github_file_url: str):
    """
    Overall
    -------
    Grabs the item from the given github repo and returns
    it as a json object.

    Returns
    -------
    A JSON object of the text of the response from github_file_url
    """
    response = requests.get(github_file_url)
    return json.loads(response.text)


def compare_items(options: dict, repo_url: str, urls: dict):
    """
    Overall
    -------
    Compares the contents of the current files with the updated contents, presumably from GitHub
    or some other raw file hosting service.

    Accepts
    -------
    - options - the items to be used
    - repo_url - the url of the repo to be referenced with
    - urls - the full urls of each file. This will be used both to compare and to get the local filenames

    Returns
    -------
    The files that need to be changed and their contents.
    Such as {filename: contents}
    """
    items_to_change = {}

    for item in options:
        # if the options declares they want to use this item
        if options[item]:
            filename_of_relevant_item = urls[item].replace(repo_url, "")

            # grab just the filename
            # and get the contents of the file with that name
            cur_item = get_option_items(filename_of_relevant_item)
            # and then compare that to the github filename's contents
            git_item = get_github_items(urls[item])

            if cur_item != git_item:
                # setting the dictionary item to equal the changes that need to be made
                items_to_change[filename_of_relevant_item] = git_item
            else:
                continue
    
    return items_to_change


def update_file(filename: str, contents: dict):
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
    ABSOLUTELY NOTHING, you scoundrel. What more do you want from me?
    Nahh there's just nothing really to return pfff.
    """
    # ...well this function was a lot shorter than I thought
    with open(filename, "w") as f:
        f.write(json.dumps(contents, indent=4))


# TEMPORARILY, this code will just support banning folks who are not already banned
# in the future, I hope for this to support all sorts of commands when interacting
# with the server, but for now I can't think of a good way to do so.
def update_server(server_ip: str, server_port: str | int, token: str, bans: dict):
    """
    Overall
    -------
    Communicates with the server to perform the given action.
    The token will need ban access so it can properly ban people.

    Returns
    -------
    The response from the server.
    """
    responses = []

    for ban in bans:
        REQUEST = {
            "API_JSON_REQUEST": {
                "Token": token,
                "Type": "Command",
                "Data": f"ban {ban} {bans[ban]}",
                # banning the user, profile, or stage
                # depending on the key of the dictionary
            }
        }

        response = request.Request(f"{server_ip}:{server_port}", json.dumps(REQUEST))
        responses.append(response.data)

    return responses
