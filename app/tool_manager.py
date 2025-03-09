import json
import time
import shodan

class ToolManager:
    def __init__(self, shodan_api_key):
        print("Initializing ToolManager...")
        self.shodan_api = shodan.Shodan(shodan_api_key)
        self.profiles = self.load_profiles()
        self.print_profiles()  # Call the method to print profiles after loading
        print("ToolManager initialized.")

    def load_profiles(self):
        try:
            with open('scanning_profiles.json', 'r') as file:
                profiles = json.load(file)
                return profiles
        except FileNotFoundError:
            print("File scanning_profiles.json not found. Returning empty profiles.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from scanning_profiles.json: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error loading profiles: {e}")
            return []

    def print_profiles(self):
        try:
            print("Loaded profiles:")
            for profile in self.profiles.get('profiles', []):
                print(f"Name: {profile['name']}, Description: {profile['description']}, Settings: {profile['settings']}")
        except Exception as e:
            print(f"Error printing profiles: {e}")

    def get_profile(self, profile_name):
        try:
            for profile in self.profiles.get('profiles', []):
                if profile['name'] == profile_name:
                    return profile
            return None
        except Exception as e:
            print(f"Error getting profile '{profile_name}': {e}")
            return None

    def use_profile(self, profile_name):
        try:
            profile = self.get_profile(profile_name)
            if profile:
                print(f"Using profile: {profile_name}")
                print(f"Settings: {profile['settings']}")
                self.perform_scan(profile['settings'])
            else:
                print(f"Profile '{profile_name}' not found.")
        except Exception as e:
            print(f"Error using profile '{profile_name}': {e}")

    def perform_scan(self, settings):
        try:
            scan_type = settings.get('scan_type', 'basic')
            timeout = settings.get('timeout', 30)
            include_subdomains = settings.get('include_subdomains', False)
            deep_scan = settings.get('deep_scan', False)
            custom_option_1 = settings.get('custom_option_1', '')
            custom_option_2 = settings.get('custom_option_2', '')

            print(f"Starting {scan_type} scan with timeout {timeout} seconds.")
            if include_subdomains:
                print("Including subdomains in the scan.")
            if deep_scan:
                print("Performing a deep scan.")

            # Build the search query based on settings
            query = "apache"
            if include_subdomains:
                query += " hostname:*"
            if custom_option_1:
                query += f" {custom_option_1}"
            if custom_option_2:
                query += f" {custom_option_2}"

            print(f"Search query: {query}")

            # Simulate scanning process
            try:
                print("Simulating scan...")
                time.sleep(timeout)
                print(f"{scan_type.capitalize()} scan completed.")
            except Exception as e:
                print(f"Error during scan simulation: {e}")

            try:
                print("Performing Shodan search...")
                results = self.shodan_api.search(query)
                self.handle_results(results, settings)
            except shodan.APIError as e:
                print(f"Shodan API error: {e}")
            except Exception as e:
                print(f"Unexpected error during Shodan search: {e}")
        except Exception as e:
            print(f"Error performing scan: {e}")

    def handle_results(self, results, settings):
        try:
            print(f"Results found: {results['total']}")
            processed_results = []
            for result in results['matches']:
                # Apply additional filtering based on settings
                if settings.get('filter_ports') and result.get('port') not in settings['filter_ports']:
                    continue
                if settings.get('filter_countries') and result.get('location', {}).get('country_code') not in settings['filter_countries']:
                    continue
                if settings.get('filter_organizations') and result.get('org') not in settings['filter_organizations']:
                    continue
                if settings.get('filter_os') and result.get('os') not in settings['filter_os']:
                    continue
                if settings.get('filter_products') and result.get('product') not in settings['filter_products']:
                    continue

                processed_result = {
                    "IP": result['ip_str'],
                    "Port": result.get('port', 'N/A'),
                    "Hostnames": result.get('hostnames', []),
                    "Location": result.get('location', {}),
                    "Organization": result.get('org', 'N/A'),
                    "Operating System": result.get('os', 'N/A'),
                    "Product": result.get('product', 'N/A'),
                    "Data": result['data']
                }
                processed_results.append(processed_result)
                print(f"IP: {processed_result['IP']}, Port: {processed_result['Port']}, Org: {processed_result['Organization']}, OS: {processed_result['Operating System']}, Product: {processed_result['Product']}, Data: {processed_result['Data'][:100]}...")  # Print first 100 chars of data

            # Save results to a file
            try:
                with open('scan_results.json', 'w') as file:
                    json.dump(processed_results, file, indent=4)
                print("Results saved to scan_results.json")
            except Exception as e:
                print(f"Error saving results: {e}")
        except Exception as e:
            print(f"Error handling results: {e}")

# Example usage
if __name__ == "__main__":
    try:
        SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
        if not SHODAN_API_KEY:
            raise ValueError("Shodan API key not found in environment variables.")
        tool_manager = ToolManager(SHODAN_API_KEY)
        tool_manager.use_profile("Default Scan")
        tool_manager.use_profile("Advanced Scan")
    except Exception as e:
        print(f"Error in example usage: {e}")