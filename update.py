from urllib import request
import json
from methods import setup
# gonna try and use urllib instead of requests so that
# the default libraries are used and no installations
# of additional libraries will be necessary.

default_opts = setup(True)

REPO = default_opts["repo_url"]
# this can be modified to whatever repo you would like to use.
# it will just append "bans.txt" or "settings.json" and so forth

# using a dictionary so that it can be a bit more dynamic
urls = {
    "bans": REPO + "bans.json",
    "settings": REPO + "public_settings.json",
    "readme": REPO + "README.md",
    # TODO: (potentially) delete for debugging
    # using this to test stuff
}

# grabbing the current banned folks
with open("options.json", "r") as opts:
    if default_opts["use_bans"]:
        with open("bans.json", "r") as b:
            bans = json.load(b)

# getting the updated list from the github
with request.urlopen(urls["bans"]) as response:
    html = response.read()

print(html.decode())
