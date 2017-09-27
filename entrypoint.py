#!/usr/local/bin/python

import os
import sys
import json
import requests

if __name__ == "__main__":
    try:
        # try legacy config (drone 0.4)
        config = json.loads(sys.argv[2]).get("vargs")
        server = config.get("server")
        app = config.get("app_config")
    except IndexError:
        # else try drone 0.5+ config
        server = os.getenv("PLUGIN_SERVER")
        app = json.loads(os.getenv("PLUGIN_APP_CONFIG"))

    r = requests.put('%s/v2/apps/%s' % (server, app.get("id")), json=app)
    print r.text
