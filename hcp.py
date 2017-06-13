"""Simple Target to play with Docker HEALTHCHECK commands
"""

import os
import platform
import sys
from bottle import Bottle, run, view, abort, response

app = Bottle(catchall=False)
hits = 0
host = platform.node()
healthy = True


@app.route('/')
@view('index_template')
def index():
    """Report number of hits and our health"""
    global hits, host, healthy
    hits += 1
    if healthy:
        return dict(hits=hits, host=host)
    else:
        abort(410, "{} is sick".format(host))


@app.route('/poison')
def poison():
    """Make this instance unhealthy so it fails the health check"""
    global healthy
    healthy = False
    return "Oh no, I'm sick"


@app.route('/die')
def die():
    """Quit this instance immediately"""
    os.abort()


@app.route('/status')
def status():
    """Machine readable"""
    global hits, host, healthy
    return {'host': host,
            'hits': hits,
            'healthy': healthy}

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=10000, quiet=False)
