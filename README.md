# Rotwood Discord RPC Mod
A sort of proof-of-concept mod for [Rotwood](https://store.steampowered.com/app/2015270/Rotwood/) to show game stats live on your Discord profile (currently unfinished).

## Have a look at it

In menus

![menu](images/menu.png)

At base camp 

![camp](images/camp.png)

Local singleplayer

![local](images/local.png)

Online

![online](images/full%20online%203%20of%204.png)

Large image text (can be disabled)

![largeimagetext](images/full%20online%203%20of%204%20with%20large%20image%20tooltip.png)

Player count can also be disabled

![playercount](images/online%20without%20player%20count.png)

# Installation
## The Mod

**Please note that this is not a usable mod, nor is it written in a valid mod format for this game. Because there's no mod loader in Rotwood yet, but also because this is my first time writing mods for Klei games so I have no experience. I will try to make this a complete mod in the future though.**

You can run the `rpc.lua` game script in Rotwood but only half of it works, Rotwood still doesn't have a REST client and cannot send/receive http requests.

### Usage
To have Rotwood load a custom script:
1. Extract the `data_script.zip` file in the game directory, there should be a new `scripts` folder.
2. Rename `data_script.zip` to something like `data_script.zip.backup` so you have something to restore back later when you dont want to run the game without any modifications (Rotwood also loads the zip file by default and you have to rename it to something else so it's forced to read the `data/` directory anyway)
3. Copy `scripts/` into `data/`. Rotwood will now load the scripts inside `data/scripts/` instead.
4. To organize custom scripts, you should make a new direcotry in `data/scripts/`, e.g: `custom/`.
5. Copy `rpc.lua` into the custom scripts folder you just made.
6. Edit `data/scripts/main.lua` and find a line that says
    ```lua
    DEV_MODE = RELEASE_CHANNEL == "dev" or IS_QA_BUILD -- For now, QA gets debug tools everywhere.
    ```
    Change it to
    ```lua
    DEV_MODE = 1
    ```
7. Start Rotwood, dev tools are now enabled, you can activate cheats and all that cool stuff.
8. Press Shift+\` to open the game console.
9. Enter the command `LoadScript("path")` where `path` is the path to that `rpc.lua` script file earlier, relative to `data/scripts/`, e.g: `custom/rpc.lua`. If nothing shows up after executing that command, it means the game loaded that script file and now you can call functions and variables within it.
10. Try running `GetRPCData()` in the console, if some json data is printed, it's working.

That's about all you can do with it for now, I will definitely complete it when the networking feature arrives.

## RPC Server Script
This is required to communicate with Discord Rich Presence server because you can't do that with the game's built in functionalities. (Klei doesn't allow you to import libraries with mods for security reasons).

The client (mod) will send game stats like current gamemode and biome name to the RPC server via http API requests (this is all done locally), then the server will use that data to interface with Discord's Rich Presence API.

### Dependencies
- [python](https://www.python.org/)
- [pypresence](https://pypi.org/project/pypresence/): for discord rpc interface.
- [flask](https://flask.palletsprojects.com/en/3.0.x/): for rest api server handling.
- [waitress](https://pypi.org/project/waitress/): to run the server.
- [requests](https://pypi.org/project/requests/): (optimal) this is for running the `send.py` and `get.py` debug scripts which are for testing only.

These can be installed through python pip, using a [pip virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) is recommended.

Install the 3 required modules for the server script to work:

```shell
pip install pypresence flask waitress
```

The `requests` module too if you want to run the debug scripts:

```shell
pip install requests
pip install requests
```

# Usage

Just run the server script:

```py
python rpc-server.py
```

It should hook into your Discord client and start waiting for update requests.

Since the game part is not finished yet, this all basically doesn't do anything. But you can manually send requests to the server and see how it works. Read through `send.py` and adjust the variables to your liking, then run it. If all goes well you will get a `204` response code in your terminal which indicates that the request went through, you should now see a game status with the set variables on your Discord profile!

You can also request the same set of data from the server at the same address for whatever purpose you want.

I plan to make it more easily customizable in the future, like adjusting what info goes where on the RPC status, for now you can go through `rpc-server.py` and make changes to your likings, There are some comments that explain how things work. If you know about modding Rotwood or Don't Starve (Together), you can tweak around to make it show other stats when the mod system comes out, the possibilities are quite endless.

# Bugs

This is my first time writing a REST api server, so it all might not go smoothly, and there's a few quirks in the code. If you do encounter any issues or instabilities, please open an issue and I will gladly look into it. Thank you!
