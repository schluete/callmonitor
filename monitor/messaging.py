#  messaging.py
#  callmonitor
#  Created by Axel Schlueter on 10.05.21.

import asyncio
from monitor.config import CONFIG
from threema.gateway import Connection, GatewayError
from threema.gateway.simple import TextMessage

async def _single_message(conn, recipient, text):
    try:
        async with conn:
            msg = TextMessage(connection=conn, to_id=recipient, text=text)
            await msg.send()
            return True
    except GatewayError as exc:
        print("Threema gateway error:", exc)
        return False

async def _all_messages(text):
    conn = Connection(
        identity=CONFIG.threema_identity,
        secret=CONFIG.threema_secret,
        verify_fingerprint=True)

    tasks = [_single_message(conn, r, text) for r in CONFIG.threema_recipients]
    return await asyncio.gather(*tasks, return_exceptions=True)

def send(text):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    return asyncio.get_event_loop().run_until_complete(_all_messages(text))