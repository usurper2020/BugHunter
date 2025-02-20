import json

class ScanningProfiles:
    """
    Manages scanning profiles for the BugHunter application.
    
    This class provides functionality to:
    - Load and save scanning profiles from/to JSON file
    - Add new scanning profiles
    - Retrieve existing profiles
    - Manage profile parameters and configurations
    
    Profiles are stored in a JSON file for persistence between
    application sessions.
    """
    
    def __init__(self, filename='scanning_profiles.json'):
        """
        Initialize the ScanningProfiles manager.
        
        Parameters:
            filename (str): Path to the JSON file storing profiles.
                          Defaults to 'scanning_profiles.json'
        """
        self.filename = filename
        self.profiles = self.load_profiles()

    def load_profiles(self):
        """
        Load scanning profiles from the JSON file.
        
        Returns:
            dict: Dictionary of profile configurations.
                 Returns empty dict if file not found.
                 
        Note:
            Silently handles file not found errors by returning
            an empty dictionary, allowing for first-time use.
        """
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_profiles(self):
        """
        Save current profiles to the JSON file.
        
        Writes the current state of profiles to disk in JSON format
        with proper indentation for readability.
        
        Note:
            Creates the file if it doesn't exist.
            Overwrites existing file if it does.
        """
        with open(self.filename, 'w') as f:
            json.dump(self.profiles, f, indent=4)

    def add_profile(self, name, parameters):
        """
        Add a new scanning profile or update existing one.
        
        Parameters:
            name (str): Name of the profile to add/update
            parameters (dict): Scanning parameters for the profile
            
        Note:
            Automatically saves profiles to disk after adding/updating.
            Overwrites existing profile if name already exists.
        """
        self.profiles[name] = parameters
        self.save_profiles()

    def get_profile(self, name):
        """
        Retrieve a specific scanning profile.
        
        Parameters:
            name (str): Name of the profile to retrieve
            
        Returns:
            dict: Profile parameters if found, None otherwise
        """
        return self.profiles.get(name, None)

    def get_all_profiles(self):
        """
        Get names of all available scanning profiles.
        
        Returns:
            list: List of profile names that are currently defined
                 in the system.
        """
        return self.profiles.keys()
