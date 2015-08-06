#!/usr/bin/env/ python
# coding: utf-8

from flask import Flask
from flask_slack import Slack
import requests
import json

app = Flask(__name__)
slack = Slack(app)
app.add_url_rule('/', view_func=slack.dispatch)

# On GCE, we're using files mounted at /secret for incoming webhook URL and team token
# Or you can hard-code values in the except blocks below.
try:
    with open('/secret/hookurl', 'r') as hookf:
        url = hookf.read().strip()
except:
    url = "https://hooks.slack.com/services/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" # <- fake ;)
try:
    with open('/secret/token', 'r') as tokenf:
        valid = tokenf.read().strip()
except:
    valid = "bZKQqL4qkCOORlwzJRAPAvNc" # phony
try:
    with open('/secret/teamid', 'r') as teamf:
        team  = teamf.read().strip()
except:
    team = "T02594HP0" # phony


@slack.command('boomshrug', token=valid,
               team_id=team, methods=['POST'])
def boomshrug(**kwargs):
    channel = kwargs.get('channel_name')
    channel = u'#%s' % channel
    input = kwargs.get('text')
    shrugji = u'💥'
    user = 'Boom'
    if ':' in input:
        shrugji = input
        user = shrugji.replace(':','').title()

    username = u'%sshrug!' % user

    # ¯\_💥_/¯ ¯\_💥_/¯ ¯\_💥_/¯
    # ============================
    boomshrug = u'¯\_%s_/¯' % shrugji
    # aw, YEAH! (•_•) / ( •_•)>⌐■-■ / (⌐■_■) ¯\_💥_/¯
    # ============================
    # ¯\_💥_/¯ ¯\_💥_/¯ ¯\_💥_/¯

    payload = {'text': boomshrug, 'username': username, 'channel': channel}
    r = requests.post(url, data=json.dumps(payload))
    return slack.response('')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



