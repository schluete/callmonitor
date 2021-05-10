#  calls.py
#  callmonitor
#  Created by Axel Schlueter on 10.05.21.

from monitor.config import CONFIG
from fritzconnection.lib.fritzcall import FritzCall

def _connect():
    return FritzCall(
        use_tls=True,
        address=CONFIG.fb_address,
        port=CONFIG.fb_port,
        user=CONFIG.fb_user,
        password=CONFIG.fb_password)

def fetch():
    calls = []
    for call in _connect().get_calls(days=7, calltype=2):
        msg = f"Verpasster Anruf von {call.Caller} "
        if call.Name:
            msg += f"({call.Name}) "
        msg += f"am {call.Date}"
        calls.append((call.Id, msg))
    return calls
