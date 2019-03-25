import requests
import rest_api.application as rest
import threading
import time

def start_rest():
    rest.app.run(host=rest.hostURL, port=rest.hostPort, debug=False)


def test_rest_server():
    t = threading.Thread(target=start_rest)

    t.start()

    number_of_tries = 0
    while number_of_tries < 10:
        try:
            r = requests.get("http://" + rest.hostURL + ":" + str(rest.hostPort) + rest.apiRoute)
            requests.get("http://" + rest.hostURL + ":" + str(rest.hostPort) + "/shutdown")
            break
        except requests.exceptions.ConnectionError:
            number_of_tries += 1
            time.sleep(0.5)

    assert(r.json is not None)

