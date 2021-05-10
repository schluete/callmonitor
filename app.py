#  app.py
#  callmonitor
#  Created by Axel Schlueter on 09.05.21.

import monitor.database as db
import monitor.messaging as msgs
import monitor.calls as calls
import flask
import logging
from monitor.config import CONFIG
from monitor.utils import is_docker
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_FILE = "monitor.log" if not is_docker() else "/log/monitor.log"

app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=10)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
logging.getLogger('werkzeug').addHandler(handler)

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
                app.logger.info(text)
                db.mark(msg_id, text)
                cnt += 1
    return f"{cnt} calls updated {datetime.now()}"
