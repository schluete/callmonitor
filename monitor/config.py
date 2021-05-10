#  config.py
#  callmonitor
#  Created by Axel Schlueter on 10.05.21.

import configparser
import os

class Config:
    def __init__(self, which):
        cfg = configparser.ConfigParser()
        cfg.read("monitor.ini")
        self._base(cfg["configuration"])
        self._recipients(cfg["recipients"])
        self._fritzbox(cfg[which])

    def _fritzbox(self, cfg):
        self.fb_address = cfg["address"]
        self.fb_port = cfg["port"]
        self.fb_user = cfg["user"]
        self.fb_password = cfg["password"]

    def _base(self, cfg):
        self.threema_identity = cfg["identity"]
        self.threema_secret = cfg["secret"]

    def _recipients(self, cfg):
        self.threema_recipients = []
        for name in cfg.keys():
            self.threema_recipients.append(cfg[name])

class CallMonitorException(Exception):
    pass

location = os.environ.get("LOCATION")
if not location:
    raise CallMonitorException("no location configured, use the LOCATION environment variable!")
CONFIG = Config(location)