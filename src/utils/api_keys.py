import os
import json

API_KEYS_DIR = "api_keys"

def save_api_key(provider, key):
    if not os.path.exists(API_KEYS_DIR):
        os.makedirs(API_KEYS_DIR)
    with open(os.path.join(API_KEYS_DIR, f"{provider.lower()}_key.json"), "w") as f:
        json.dump({"api_key": key}, f)

def load_api_key(provider):
    key_file = os.path.join(API_KEYS_DIR, f"{provider.lower()}_key.json")
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            return json.load(f).get("api_key")
    return None
