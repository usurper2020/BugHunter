import shodan
from typing import Dict, List, Optional
import json
import os

class ShodanIntegration:
    """Handles integration with Shodan API for security intelligence"""
    
    def __init__(self, api_key: str = ''):
        self.api_key = api_key
        self.api = None
        if api_key:
            self.api = shodan.Shodan(api_key)
        self.results_dir = os.path.join('data', 'shodan_results')
        os.makedirs(self.results_dir, exist_ok=True)
        
    def set_api_key(self, api_key: str) -> Dict:
        """Set or update the Shodan API key"""
        try:
            self.api_key = api_key
            self.api = shodan.Shodan(api_key)
            return {
                "status": "success",
                "message": "API key updated successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def search_host(self, ip: str) -> Dict:
        """Search for information about a specific IP"""
        if not self.api:
            return {
                "status": "error",
                "message": "API key not configured"
            }
            
        try:
            results = self.api.host(ip)
            
            # Save results
            filename = os.path.join(self.results_dir, f"host_{ip}.json")
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            return {
                "status": "success",
                "data": results,
                "saved_to": filename
            }
        except shodan.APIError as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def search_query(self, query: str, limit: int = 100) -> Dict:
        """Search Shodan using a query string"""
        if not self.api:
            return {
                "status": "error",
                "message": "API key not configured"
            }
            
        try:
            results = self.api.search(query, limit=limit)
            
            # Save results
            filename = os.path.join(
                self.results_dir, 
                f"search_{query.replace(' ', '_')}.json"
            )
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
                
            return {
                "status": "success",
                "data": results,
                "saved_to": filename
            }
        except shodan.APIError as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_ports(self, ip: str) -> Dict:
        """Get open ports for a specific IP"""
        if not self.api:
            return {
                "status": "error",
                "message": "API key not configured"
            }
            
        try:
            host = self.api.host(ip)
            ports = list(set([service['port'] for service in host['data']]))
            
            return {
                "status": "success",
                "ports": sorted(ports)
            }
        except shodan.APIError as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_vulnerabilities(self, ip: str) -> Dict:
        """Get vulnerabilities for a specific IP"""
        if not self.api:
            return {
                "status": "error",
                "message": "API key not configured"
            }
            
        try:
            host = self.api.host(ip)
            vulns = host.get('vulns', [])
            
            # Get details for each vulnerability
            vuln_details = []
            for vuln_id in vulns:
                try:
                    details = self.api.exploits.search(vuln_id)
                    vuln_details.append({
                        "id": vuln_id,
                        "details": details
                    })
                except:
                    vuln_details.append({
                        "id": vuln_id,
                        "details": "Details not available"
                    })
                    
            return {
                "status": "success",
                "vulnerabilities": vuln_details
            }
        except shodan.APIError as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def scan_ip(self, ip: str) -> Dict:
        """Request Shodan to scan an IP"""
        if not self.api:
            return {
                "status": "error",
                "message": "API key not configured"
            }
            
        try:
            scan_id = self.api.scan(ip)
            return {
                "status": "success",
                "scan_id": scan_id
            }
        except shodan.APIError as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_scan_status(self, scan_id: str) -> Dict:
        """Get the status of a scan"""
        if not self.api:
            return {
                "status": "error",
                "message": "API key not configured"
            }
            
        try:
            status = self.api.scan_status(scan_id)
            return {
                "status": "success",
                "scan_status": status
            }
        except shodan.APIError as e:
            return {
                "status": "error",
                "message": str(e)
            }
