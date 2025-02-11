import json

class ScanningProfiles:
    def __init__(self, filename='scanning_profiles.json'):
        self.filename = filename
        self.profiles = self.load_profiles()

    def load_profiles(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_profiles(self):
        with open(self.filename, 'w') as f:
            json.dump(self.profiles, f, indent=4)

    def add_profile(self, name, parameters):
        self.profiles[name] = parameters
        self.save_profiles()

    def get_profile(self, name):
        return self.profiles.get(name, None)

    def get_all_profiles(self):
        return self.profiles.keys()
