#!/usr/local/bin/python3.6

from rest_api.application import app, hostURL, hostPort

if __name__ == "__main__":
    app.run(host=hostURL, port=hostPort, debug=True)
