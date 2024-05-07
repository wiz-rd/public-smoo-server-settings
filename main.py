import sys
from helper import APIHandler, setup, compare_and_update_bans

# options's keys are as follows:
# repo_url
# token
# host
# port
options = setup()

"""
The items to not ban.
May make this (e.g. stages, ip addresses etc) an option sometime.
"""
SKIP_BANS_FOR = (
    # "Enabled" should always be skipped
    "Enabled",
    "Stages",
    # These should not be enabled by default.
    # "Players",
    # "IpAddresses",
)

handler = APIHandler(options["host"], options["port"], options["token"])
print(handler)

differing_items = compare_and_update_bans(options["repo_url"])

if differing_items is None:
    sys.exit("Your bans are up to date!")
else:
    # going through each method of banning
    for method, item in differing_items.items():
        # if it's not one of the ones we want to ban (for example, stages), skip it
        if method in SKIP_BANS_FOR:
            continue

        # going through each ban themselves
        if type(item) == list:
            for it in item:
                if method == "Players":
                    print(handler.ban("profile", it))
                elif method == "IpAddresses":
                    print(handler.ban("ip", it))
