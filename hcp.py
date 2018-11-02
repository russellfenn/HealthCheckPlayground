"""Simple Target to play with Docker HEALTHCHECK commands
"""

from bottle import Bottle, run, view, abort, Response
from prometheus_client import core, Counter, Gauge
from prometheus_client.exposition import generate_latest
import os
import platform
import sys
import time

app = Bottle(catchall=False)
hits = 0
node = platform.node()
healthy = True

request_counter = Counter('request_counter', 'Total requests', ['node', 'route'])
node_health = Gauge('node_health', 'Poisoned or not', ['node'])
node_health.labels(node=node).set("1.0")

@app.route('/')
@view('index_template')
def index():
    """Report number of hits and our health"""
    global hits, node, healthy
    hits += 1
    request_counter.labels(node=node, route='/').inc()
    if healthy:
        return dict(hits=hits, node=node)
    else:
        abort(410, f"{node} is sick")


@app.route('/poison')
def poison():
    """Make this instance unhealthy so it fails the health check"""
    global healthy
    healthy = False
    request_counter.labels(node=node, route='/poison').inc()
    node_health.labels(node=node).set("0.0")
    return f"I'm {node} and I don't feel well"


@app.route('/die')
def die():
    """Quit this instance immediately"""
    os.abort()


@app.route('/status')
def status():
    """Machine readable"""
    global hits, node, healthy
    request_counter.labels(node=node, route='/status').inc()
    return {'node': node,
            'hits': hits,
            'healthy': healthy}


@app.route('/metrics')
def metrics():
    """Return Prometheus metrics"""
    return generate_latest()
    response = Response()
    response.set_header('Content-Type', 'text/plain; version=0.0.4; charset=utf-8')
    response.body = generate_latest()
    return response

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=10000, quiet=False)
