#!/usr/local/bin/python

import os
import re
import sys
import json
import requests


def replace_secrets(d):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            replace_secrets(v)
        elif isinstance(v, str):
            if v[0:1] == "${" and v[-1] == "}":
                v = re.sub('[\$\{\}]', '', v)


if __name__ == "__main__":
    try:
        # try legacy config (drone 0.4)
        config = json.loads(sys.argv[2]).get("vargs")
        server = config.get("server")
        app = config.get("app_config")
        print "Running legacy version (Drone 0.4)"
    except IndexError:
        # else try drone 0.5+ config
        server = os.getenv("PLUGIN_SERVER")
        app = json.loads(os.getenv("PLUGIN_APP_CONFIG"))

    print json.dumps(app, indent=4)
    replace_secrets(app)
    r = requests.put('%s/v2/apps/%s' % (server, app.get("id")), json=app)
    print r.text
