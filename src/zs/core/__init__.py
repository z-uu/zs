import os
import sys
import json
ZS_EXE_PATH = os.path.dirname(sys.executable)
APP_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".zs")

def get_installed():
    for exep in os.listdir(ZS_EXE_PATH):
        if not os.path.isfile(os.path.join(ZS_EXE_PATH, exep)):
            continue
        if not exep.endswith(".exe"):
            continue

        if exep in ["zs.kvstore.exe"]:
            continue

        if not exep.startswith("zs."):
            continue

        yield exep.replace(".exe", "")

INSTALLED = list(get_installed())

INDEX = json.load(open(os.path.join(os.path.dirname(__file__), "index.json")))