#!/usr/bin/env/ python3
# coding: utf-8
import json
import os

import requests

from flask import Flask
from flask_slack import Slack

app = Flask(__name__)
slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)

# Currently, we mount our secrets as environment variables across
# our services, therefore variables can either be hardcoded here
# or defined in the environment
# PS: all of these are phony hardcodes ;)
url = os.getenv('HOOKURL', "https://hooks.slack.com/services/"
                           "T02594HP0/B081REU01/PjOvu5UAGNgVKUTydc3GqS6L")
valid = os.getenv('TOKEN', 'bZKQqL4qkCOORlwzJRAPAvNc')
team = os.getenv('TEAM_ID', 'T02594HP0')

@slack.command('boomshrug', token=valid,
               team_id=team, methods=['POST'])
def boomshrug(**kwargs):
    channel = kwargs.get('channel_id')
    input = kwargs.get('text')
    shrugji = '💥'
    user = 'Boom'
    if ':' in input:
        shrugji = input
        user = shrugji.replace(':', '').title()

    username = '{}shrug!'.format(user)

    # ¯\_💥_/¯ ¯\_💥_/¯ ¯\_💥_/¯
    # ============================
    boomshrug = '¯\_{}_/¯'.format(shrugji)
    # aw, YEAH! (•_•) / ( •_•)>⌐■-■ / (⌐■_■) ¯\_💥_/¯
    # ============================
    # ¯\_💥_/¯ ¯\_💥_/¯ ¯\_💥_/¯

    payload = {'text': boomshrug, 'username': username, 'channel': channel}
    r = requests.post(url, data=json.dumps(payload))
    return slack.response('')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
