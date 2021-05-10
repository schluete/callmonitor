#  app.py
#  callmonitor
#  Created by Axel Schlueter on 09.05.21.

import monitor.database as db
import monitor.messaging as msgs
import monitor.calls as calls
import flask
from monitor.config import CONFIG
from datetime import datetime

app = flask.Flask(__name__)

@app.route('/')
def status():
    return 'Hello, Docker!'

@app.route('/test')
def testing():
    msgs.send(f"for all {datetime.now()}")
    return f"boom {datetime.now()}"

@app.route('/crash')
def crash():
    return f"boom {datetime.now()}", 400

@app.route('/update')
def update():
    cnt = 0
    for (msg_id, text) in calls.fetch():
        if not db.check(msg_id):
            if msgs.send(text):
                print(text)
                db.mark(msg_id, text)
                cnt += 1
    return f"{cnt} calls updated {datetime.now()}"
