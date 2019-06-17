#!/usr/local/bin/python3.6

import sys, getopt 

from rest_api.general_application import app as g_app, hostURL as g_hostURL, hostPort as g_hostPort
from rest_api.music_application import app as m_app, hostURL as m_hostURL, hostPort as m_hostPort
from rest_api.video_application import app as v_app, hostURL as v_hostURL, hostPort as v_hostPort


def main(argv):
    type = ""

    try:
      opts, args = getopt.getopt(argv, "ht:", ["help", "type="])
    except getopt.GetoptError:
        print('__main__.py -t <api_type>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "help"):
            print('__main__.py -t <api_type>')
            sys.exit()
        elif opt in ('-t', "--type"):
            type = arg

    if type in ("general", ""):
        g_app.run(host=g_hostURL, port=g_hostPort, debug=False)
    elif type == "music":
        m_app.run(host=m_hostURL, port=m_hostPort, debug=False)
    elif type == "video":
        v_app.run(host=v_hostURL, port=v_hostPort, debug=False)


if __name__ == "__main__":
    main(sys.argv[1:])
