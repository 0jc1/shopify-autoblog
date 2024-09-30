import json
import os
import sys

config_file = 'config.json'

# ConfigManager singleton
class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def read_config(self):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Config file {config_file} not found.")

    def write_config(self, config):
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def update_config(self, key, value):
        config = self.read_config()
        config[key] = value
        self.write_config(config)

    def delete_key(self, key):
        config = self.read_config()
        if key in config:
            del config[key]
            self.write_config(config)

config = ConfigManager().read_config()
