# DEBUG SCRIPT (not used in production)

# this is how the json data sent to the rpc server
# should look like, with all keys included in samplejson_full
# and different use cases below where some unnecessary keys can
# be removed accordingly

import requests

# templates/examples

# full form
samplejson_full = { # (online, 3/4 players, nocturne grove biome)
	"ingame" : True, # false if in menu, true if in gameplay
 	"localgame" : False, # true if playing locally, false if playing in online mode
	"room" : "sample_room_name_12345", # (optimal) room name
	"biome" : "Nocturne Grove", # pretty biome name
 	"playercount" : 3, # (optimal) party player count / 4
	"clearrpc" : False # (optimal) set to true to signal rpc server to clear rpc status
}

# example ingame local
samplejson_local = { # (local singleplayer)
	"ingame" : True,
 	"localgame" : True,
  	"room" : "sample_room_name_12345",
	"biome" : "Nocturne Grove",
 	"playercount" : 1,
}

samplejson_camp = { # (local 2 players, at base camp)
	"ingame" : True,
 	"localgame" : True,
  	"room" : "sample_room_name_12345",
	"biome" : "Camp",
 	"playercount" : 2,
}

# example ingame online
samplejson_online = { # (online 2 players)
	"ingame" : True,
 	"localgame" : False,
	"room" : "sample_room_name_12345",
	"biome" : "Blisterbane Bog",
 	"playercount" : 2,
}

# example ingame without player count
# you can remove the playercount key or set it to 0
# if you dont want to show the party size on discord
samplejson_online_no_playercount = { # (online game, party size hidden/disabled)
	"ingame" : True,
 	"localgame" : False,
	"room" : "sample_room_name_12345",
	"biome" : "Blisterbane Bog",
 	# "playercount" : 2,
}

# example ingame without room name on large image
# you can leave the room key empty "" or not include it
# to not show the room name when large image is hovered
samplejson_online_no_roomname = { # (online 2 players, room name hidden)
	"ingame" : True,
 	"localgame" : False,
	# "room" : "sample_room_name_12345",
	"biome" : "Blisterbane Bog",
 	"playercount" : 2,
}

# menu
# you can make rpc only says "In Menu"
# by requesting an update with the following data
samplejson_menu = {
    "ingame" : False
}

# clear rpc status
samplejson_rpcclear = {
    "rpcclear" : True
}

r = requests.post("http://0.0.0.0:1974/api/rotwoodrpc", json=samplejson_full)
print(r.status_code)
