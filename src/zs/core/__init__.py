import os
import sys

ZS_EXE_PATH = os.path.dirname(sys.executable)
APP_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".zs")

def get_installed():
    for exep in os.listdir(ZS_EXE_PATH):
        if not os.path.isfile(os.path.join(ZS_EXE_PATH, exep)):
            continue
        if not exep.endswith(".exe"):
            continue

        if not exep.startswith("zs."):
            continue

        yield exep

INSTALLED = list(get_installed())