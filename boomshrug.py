#!/usr/bin/env/ python
# coding: utf-8

from flask import Flask
from flask_restful import Resource, Api
# from flask.ext.api import status
import requests
import json
import cherrypy
from paste.translogger import TransLogger

app = Flask(__name__)
api = Api(app)

class BoomShrug(Resource):
    def get(self):
        boomshrug = u'¯\_:boom:_/¯'
        payload = {'text': boomshrug}
        really = None
        url = 'https://hooks.slack.com/services/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'
        r = requests.post(url, data=json.dumps(payload))
        return ('', 204)
api.add_resource(BoomShrug, '/')

def run_server():
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload_on': True,
        'environment': 'embedded',
        'log.screen': True,
        'server.socket_port': 5000,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server

    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == "__main__":
    run_server()
