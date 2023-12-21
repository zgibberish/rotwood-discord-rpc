# DEBUG SCRIPT (not used in production)

# fetches game data from the rpc server script through
# http GET request

from pprint import pprint
import requests

r = requests.get("http://0.0.0.0:1974/api/rotwoodrpc")
pprint(r.json())
