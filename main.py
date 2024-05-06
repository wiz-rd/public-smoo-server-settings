import sys
from helper import BanHandler, setup, compare_and_update

# options's keys are as follows:
# repo_url
# token
# host
# port
options = setup()
banhandler = BanHandler(options["host"], options["port"], options["token"])

differing_items = compare_and_update(options["repo_url"])

if differing_items is None:
    sys.exit("Your bans are up to date.")
else:
    for method, argument in differing_items.items():
        # will need to fill this in at a later time.
        # NOTE: differing_items does NOT actually contain just the player and/or IP list...
        # I need to update this to reflect that.......... oops pfff
        pass
