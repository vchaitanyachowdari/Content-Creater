import os
import yaml

class Config:
    """Configuration management class"""
    
    def __init__(self, config_file='config/config.yaml'):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        """Load configuration from YAML file"""
        with open(self.config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get(self, key, default=None):
        """Get a configuration value"""
        return self.config.get(key, default) 