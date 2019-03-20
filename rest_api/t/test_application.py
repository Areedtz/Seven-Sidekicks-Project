import requests
import rest_api.application as rest
import threading
import time

def start_rest():
    rest.app.run(host=rest.hostURL, port=rest.hostPort, debug=False)

t = threading.Thread(target=start_rest)
t.start()

time.sleep(2)

r = requests.get("http://" + rest.hostURL + ":" + str(rest.hostPort) + rest.apiRoute)
        
assert(r.json is not None)

