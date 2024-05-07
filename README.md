# public-smoo-server-settings
A bundle of settings for the (Super Mario Odyssey Online mod's)[https://github.com/CraftyBoss/SuperMarioOdysseyOnline] (server)[https://github.com/Sanae6/SmoOnlineServer] (see below regarding server version) that can be used to share banned players and IPs and sync with static files on the web.

# Prerequisites

Requirements
- A version of the server that has the JSON API enabled, such as [RCL's](https://github.com/Istador/SmoOnlineServer/tree/1.0.5-rcl.3)
- Have Python 3.x installed
- Have the requests library installed (`pip install requests`)

# Setup

Find your server file.
- Ensure you have BanList enabled in your server settings.json (this should be enabled when a request is made but it might not be)
- Create a token for this program (also in settings.json)
- Give it [appropriate authority](https://github.com/Istador/SmoOnlineServer/blob/1.0.5-rcl.3/Server/JsonApi/README.md). Scroll down until you see "Example for the settings.json:" for an example
- Download or clone this repo (on the top right of this page, click "Code" and then "Download Zip" if you're unsure)
- Run main.py
