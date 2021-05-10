#  utils.py
#  callmonitor
#  Created by Axel Schlueter on 10.05.21.

import os

def is_docker():
    path = '/proc/self/cgroup'
    return (os.path.exists('/.dockerenv') or
            os.path.isfile(path) and any('docker' in line for line in open(path)))
