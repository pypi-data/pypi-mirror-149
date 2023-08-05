"""
Wrapper (with monkeypatched behaviour) for original pycsw WSGI application object
"""

# Imports from . import * are needed to override original PyCSW behaviour
# pylint: disable=W0611

import sys

from pycsw.wsgi import application

from . import apiso, config, metadata

if __name__ == "__main__":  # run inline using WSGI reference implementation

    from wsgiref.simple_server import make_server

    PORT = 8000
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    httpd = make_server("", PORT, application)
    print("Serving on port {}...".format(PORT))
    httpd.serve_forever()
