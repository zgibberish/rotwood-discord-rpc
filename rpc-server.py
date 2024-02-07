import pypresence
import time    
from flask import Flask, request, jsonify

appID = "1185955546084429876"
RotwoodRPC = pypresence.Presence(appID)
Game = {} # dictionary that stores game stats sent by the game
app = Flask(__name__)

def connectRPC():
    # returns true when connection is made successfuly
    # returns false when an exception is caught
    try:
        RotwoodRPC.connect()
    except Exception as exc:
        print(f"    exception caught while connecting rpc: {exc}")
        return False
    else:
        print("    rpc connected")
        return True

def updateRPC():    
    p_details = None
    p_state = None
    p_party_size = None
    p_large_text = None
    
    # edit the part below if you want to change
    # what goes where on the rich presence status.
    
    # if you decide to add additional data, you will
    # have to write the appropriate logic for them
    # (in both game side and server side).
    # and you should nil check them as always
    # it is also good to have fallback values.
    if (Game["ingame"]):
        # i dont need to nil check these keys
        # because its not meant to be missing
        # from the game stats dictionary by default.
        if (Game["localgame"]):
            p_state =  "Playing Local"
        else:
            p_state =  "Playing Online"

        p_details =  Game["biome"]
        
        # these keys below have to be nil checked because
        # i made them to be optional, which means
        # you can disable/hide them on your rich presence
        # by leaving them empty, zero or not provided at all.
        if ("room" in Game):
            if (Game["room"] != ""):
                p_large_text = Game["room"]
            else:
                p_large_text = None
        if ("playercount" in Game):
            if (Game["playercount"] == 0):
                p_party_size = None
            else:
                p_party_size = [Game["playercount"], 4]
        else:
            p_party_size = None
    else:
        p_details =  "In Menus"

    # for loop that loops three times so if something goes wrong it can
    # try again (like when RPC fails and needs to be reconnected)
    for i in range(2):
        try:
            RotwoodRPC.update(
                large_image="library_hero_512",
                details=p_details,
                state=p_state,
                party_size=p_party_siz
                large_text=p_large_text
            )
        except Exception as exc:
            print(f"    exception caught while updating rpc status: {exc}")
            print("    trying to reconnect rpc")
            
            # retry connection every 2 secs for 10 times
            connectionSuccess = False
            for j in range(10):
                connectionSuccess = connectRPC()
                if connectionSuccess:
                    break
                # safe time delay
                time.sleep(2)
                
            # retry update process anyway regardless if
            # connection was success or not
        else:
            print("    rpc updated")
            break
        # again, safe time delay
        time.sleep(1)

@app.route("/api/rotwoodrpc", methods=["POST", "GET"])
def api_handler():
    if request.method == "POST":
        global Game
        Game = request.get_json()
        
        # "rpcclear" is the boolean signal to clear the rpc status,
        # you should not use it for anything else.
        # rpc is cleared but not closed so it can be shown again
        # simply be refreshing it (update) with new data
        if ("rpcclear" in Game) and (Game["rpcclear"]):
            print("    rpc termination triggered")
            try:
                RotwoodRPC.clear()
                print("    rpc cleared")
            except Exception as exc:
                print(f"    exception caught while clearing rpc: {exc}")
            finally:
                return '', 204
        
        print("updating rpc...")
        try:
            updateRPC()
        except Exception as exc:
            print(f"    exception caught when calling updateRPC() from api_handler: {exc}")
        
        return '', 204
        # notes:
            # HTTP Status 204 (No Content) indicates that
            # the server has successfully fulfilled the request
            # and that there is no content to send
            # in the response payload body.
    else:
        return jsonify(Game)

if __name__ == "__main__":
    # try until connection success
    print("connecting rpc")
    while (True):
        connectionSuccess = connectRPC()
        if connectionSuccess:
            break
        # safe time delay
        time.sleep(2)

    # web server starts from here
    from waitress import serve
    serve(app, host="0.0.0.0", port=1974)
    # code down here wont be executed
    # until after the server stops (unstable)
