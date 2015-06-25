#!/usr/bin/env/ python
# coding: utf-8

from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
import json
import cherrypy
from paste.translogger import TransLogger

app = Flask(__name__)
api = Api(app)

class BoomShrug(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('channel_name', type=unicode)
        parser.add_argument('token', type=unicode)
        parser.add_argument('text', type=unicode)
        args = parser.parse_args()
        channel = args.channel_name
        token = args.token
        if args.text:
            thisshrug = args.text
        else:
            thisshrug = u'💥'


        # ¯\_💥_/¯ ¯\_💥_/¯ ¯\_💥_/¯
        # ============================
        boomshrug = u'¯\_%s_/¯' % thisshrug # aw, YEAH! (•_•) / ( •_•)>⌐■-■ / (⌐■_■) ¯\_💥_/¯
        # ============================
        # ¯\_💥_/¯ ¯\_💥_/¯ ¯\_💥_/¯

        # On GCE, we're using files mounted at /secret for incoming webhook URL and team token
        # Or you can hard-code values in the except blocks below.
        try:
            with open('/secret/hookurl', 'r') as hookf:
                url = hookf.read().strip()
        except:
            url = "https://hooks.slack.com/services/Qm09HXTQ6W/Qm09HXTQ6W/Qm09HXTQ6WQm09HXTQ6W" # <- fake ;)
        try:
            with open('/secret/token', 'r') as tokenf:
                valid = tokenf.read().strip()
        except:
            valid = "Qm09HXTQ6WUPPuMo6pBQhVh4" # phony

        #Only accept posts from our team
        if token != valid:
            return ('naughty, naughty!', 403)
        else: # Send the boomshrug!!
            if channel != 'directmessage':
                channel = u'#%s' % channel
                payload = {'text': boomshrug, 'channel': channel}
                r = requests.post(url, data=json.dumps(payload))
                return ('', 204)
            else: # I don't know how to make this work for directmessages :/
                return(u'whoops, only works in a public channel. sorry :(', 200)

api.add_resource(BoomShrug, '/')

def run_server():
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
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
