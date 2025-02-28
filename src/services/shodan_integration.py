"""
Shodan integration for the BugHunter application.
Provides functionality for querying Shodan's database.
"""

import logging
import shodan
from typing import List, Dict, Optional

class ShodanIntegration:
    """Manages integration with the Shodan API"""
    
    def __init__(self, api_key: str):
        self.logger = logging.getLogger('BugHunter.ShodanIntegration')
        self.api = shodan.Shodan(api_key)
        
    def search(self, query: str) -> List[Dict[str, any]]:
        """
        Search Shodan's database
        
        Args:
            query: Search query string
            
        Returns:
            List of search results
        """
        try:
            results = self.api.search(query)
            self.logger.info(f"Found {results['total']} results for query: {query}")
            return results['matches']
        except shodan.APIError as e:
            self.logger.error(f"Shodan API error: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Failed to search Shodan: {str(e)}")
            return []
            
    def get_host(self, ip: str) -> Optional[Dict[str, any]]:
        """
        Get information about a specific host
        
        Args:
            ip: IP address of the host
            
        Returns:
            Dictionary containing host information if found, None otherwise
        """
        try:
            host = self.api.host(ip)
            return host
        except shodan.APIError as e:
            self.logger.error(f"Shodan API error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get host info: {str(e)}")
            return None
            
    def get_ports(self) -> List[int]:
        """
        Get list of ports that Shodan is listening on
        
        Returns:
            List of port numbers
        """
        try:
            ports = self.api.ports()
            return ports
        except shodan.APIError as e:
            self.logger.error(f"Shodan API error: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Failed to get ports: {str(e)}")
            return []
            
    def get_protocols(self) -> List[str]:
        """
        Get list of protocols that Shodan understands
        
        Returns:
            List of protocol names
        """
        try:
            protocols = self.api.protocols()
            return protocols
        except shodan.APIError as e:
            self.logger.error(f"Shodan API error: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Failed to get protocols: {str(e)}")
            return []
            
    def get_scan_status(self) -> Dict[str, any]:
        """
        Get information about the Shodan scan status
        
        Returns:
            Dictionary containing scan status information
        """
        try:
            status = self.api.scan_status()
            return status
        except shodan.APIError as e:
            self.logger.error(f"Shodan API error: {str(e)}")
            return {}
        except Exception as e:
            self.logger.error(f"Failed to get scan status: {str(e)}")
            return {}
