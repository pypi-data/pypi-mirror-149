import json
import os
import warnings

class KeyHold:
    def __init__(self, path, create=False):
        self.path = path
        self.create = create
        
        self._dict = {}
        
        if self.create:
            self.ensure_configfile(path)
        
        self.load()

    def ensure_configfile(self, path):
        if os.path.exists(path):
            return
        
        if not self.create:
            raise ValueError('config file not exists')
        
        with open(path, 'w'):
            warnings.warn(RuntimeWarning('new config file created'))
    
    def __repr__(self):
        return str(self._dict)
    
    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, val):
        self._dict[key] = val
    
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self._dict, f, indent=2)
    
    def load(self):
        with open(self.path, 'r') as f:
            try:
                self._dict = json.load(f)
            except:
                self._dict = {}
