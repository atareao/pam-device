import os
from os.path import expanduser


CONFIG_DIR = os.path.join(expanduser('~'), '.config', 'pam-device')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'pam-device.json')
PARAMS = {'usb': [],
          'bluetooth-scan-timeout': 8,
          'bluetooth-check-timeout': 2,
          'bluetooth': []}