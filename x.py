import os
from src.zs.core import APP_CONFIG_PATH

PATH = os.path.join(APP_CONFIG_PATH, "kvstore", "index.json")

os.system(f"cursor {PATH}")