#!venv/bin/python

# To do call monitoring, the CallMonitor service of the Fritz!Box has to be activated.
# This can be done with any registered phone by typing the following codes:
# activate: #96*5*
# deactivate: #96*4*

# > telnet 192.168.0.1 1012
# Trying 192.168.0.1...
# Connected to fritz.box.
# Escape character is '^]'.
# 09.05.21 21:21:25;RING;0;012345678901;01234567;SIP2;
# 09.05.21 21:21:27;DISCONNECT;0;0;
# 09.05.21 21:21:35;RING;0;012345678901;01234567;SIP2;
# 09.05.21 21:21:36;CONNECT;0;13;012345678901;
# 09.05.21 21:21:41;DISCONNECT;0;2;

# https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353

from contextlib import contextmanager
from fritzconnection.lib.fritzcall import FritzCall
from threema.gateway import Connection, GatewayError
from threema.gateway.simple import TextMessage
import configparser
import sqlite3


@contextmanager
def database():
    conn = sqlite3.connect("monitor.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS calls (msg_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, text VARCHAR)")
    conn.commit()
    try:
        yield conn
    finally:
        conn.close()

def check_for_message(msg_id):
    with database() as db:
        rs = db.cursor().execute(f"SELECT count(*) FROM calls WHERE msg_id = {msg_id}").fetchone()
        return rs[0] > 0

def mark_message(msg_id, text):
    with database() as db:
        db.cursor().execute("INSERT INTO calls VALUES(?, ?)", (msg_id, text))
        db.commit()

def message(recipient, text):
    # conn = Connection(
    #     identity="*5V9ROBO",
    #     secret="YOUR_GATEWAY_THREEMA_ID_SECRET",
    #     verify_fingerprint=True,
    #     blocking=True)

    # msg = TextMessage(connection=conn, to_id=dest, text=text)
    # result = msg.send()
    # print(result)
    print(f"{recipient}: {text}")
    return True

def connect(settings):
    return FritzCall(
        use_tls=True,
        address=settings["address"],
        port=settings["port"],
        user=settings["user"],
        password=settings["password"])

def fetch_calls(fc):
    calls = []
    for call in fc.get_calls(days=7, calltype=2):
        msg = f"Verpasster Anruf von {call.Caller} "
        if call.Name:
            msg += f"({call.Name}) "
        msg += f"am {call.Date}"
        calls.append((call.Id, msg))
    return calls

def main():
    cfg = configparser.ConfigParser()
    cfg.read("monitor.ini")
    recipient = cfg["default"]["recipient"]

    settings = cfg["lenauweg"]
    fc = connect(settings)
    calls = fetch_calls(fc)

    for (msg_id, text) in calls:
        if not check_for_message(msg_id):
            if message(recipient, text):
                mark_message(msg_id, text)

if __name__ == "__main__":
    main()
