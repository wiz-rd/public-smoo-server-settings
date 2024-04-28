from methods import setup, compare_items, update_file, update_server

custom_options = setup(True)

# REPO = custom_options["repo_url"]
# this can be modified to whatever repo you would like to use.
# it will just append "bans.txt" or "settings.json" and so forth

urls = {}

for file in custom_options["use"]:
    urls[file] = custom_options["repo_url"] + file

# # using a dictionary so that it can be a bit more dynamic
# urls = {
#     "bans": REPO + "bans.json",
#     "readme": REPO + "README.md",
#     # TODO: (potentially) delete for debugging
#     # using this to test stuff
# }

# grabbing the current banned folks
# and getting the updated list from the github
updates_to_be_made = compare_items(custom_options["use"], custom_options["repo_url"], urls)

for up in updates_to_be_made:
    print(f"Changes found in {up}, updating now.")
    update_file(up, updates_to_be_made[up])

if len(updates_to_be_made) > 0:
    print("Attempting to reload the server...")
    s_response = update_server(custom_options["host"], custom_options["port"], custom_options["token"])
    print(f"Server response: {s_response}")
