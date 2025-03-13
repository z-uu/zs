import re
import os
import json
from zs.core import APP_CONFIG_PATH
from zs.kvstore.fileprop import fileProperty
PATH = os.path.join(APP_CONFIG_PATH, "kvstore", "store.json")
if not os.path.exists(PATH):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)

class _KVStore:
    PATH = PATH
    STORE = fileProperty(PATH)  

    def get(self, key : str, default = None):
        return self.STORE.get(key, default)

    def set(self, key : str, value):
        self.STORE[key] = value
    
    def delete(self, key : str):
        if key not in self.STORE:
            return
        data = self.STORE.copy()
    
        del data[key]
        self.STORE = data

    def clear(self):
        self.STORE.clear()

    def keys(self):
        yield from self.STORE.keys()

    def values(self):
        yield from self.STORE.values()

    def items(self):
        yield from self.STORE.items()

KVStore = _KVStore()


def parse_document(document : str):
    pattern = r'<\$@(\w+)>'
    matches = re.findall(pattern, document)
    
    for match in matches:
        key = match
        snippet = KVStore.get(key)
        
        if snippet is None:
            raise ValueError(f"Key {key} not found in store")
        document = re.sub(r'^//<\$@' + re.escape(key) + '>', f'<$@{key}>', document, flags=re.MULTILINE)
        document = re.sub(r'^#<\$@' + re.escape(key) + '>', f'<$@{key}>', document, flags=re.MULTILINE)
        document = document.replace(f'<$@{key}>', snippet)
        
    return document
