import requests
from typing import Dict, List, Optional
from datetime import datetime
import json
import os

class WaybackMachineIntegration:
    """Handles integration with Internet Archive's Wayback Machine"""
    
    def __init__(self):
        self.base_url = "https://archive.org/wayback/available"
        self.results_dir = os.path.join('data', 'wayback_results')
        os.makedirs(self.results_dir, exist_ok=True)
        
    def search_url(self, url: str, timestamp: Optional[str] = None) -> Dict:
        """Search for archived versions of a URL"""
        try:
            params = {'url': url}
            if timestamp:
                params['timestamp'] = timestamp
                
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save results
            filename = os.path.join(
                self.results_dir, 
                f"wayback_{url.replace('://', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
                
            return {
                "status": "success",
                "data": data,
                "saved_to": filename
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_snapshots(self, url: str) -> Dict:
        """Get all available snapshots for a URL"""
        try:
            cdx_url = f"https://web.archive.org/cdx/search/cdx"
            params = {
                'url': url,
                'output': 'json',
                'fl': 'timestamp,original,mimetype,statuscode,digest'
            }
            
            response = requests.get(cdx_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Process the data
            if not data or len(data) < 2:  # First row is header
                return {
                    "status": "success",
                    "snapshots": []
                }
                
            header = data[0]
            snapshots = [dict(zip(header, row)) for row in data[1:]]
            
            # Save results
            filename = os.path.join(
                self.results_dir, 
                f"snapshots_{url.replace('://', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(filename, 'w') as f:
                json.dump(snapshots, f, indent=2)
                
            return {
                "status": "success",
                "snapshots": snapshots,
                "saved_to": filename
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_snapshot_content(self, url: str, timestamp: str) -> Dict:
        """Get the content of a specific snapshot"""
        try:
            wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"
            response = requests.get(wayback_url)
            response.raise_for_status()
            
            # Save content
            filename = os.path.join(
                self.results_dir, 
                f"content_{url.replace('://', '_').replace('/', '_')}_{timestamp}.html"
            )
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
                
            return {
                "status": "success",
                "content": response.text,
                "saved_to": filename
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def compare_snapshots(self, url: str, timestamp1: str, timestamp2: str) -> Dict:
        """Compare two snapshots of the same URL"""
        try:
            snapshot1 = self.get_snapshot_content(url, timestamp1)
            if snapshot1["status"] == "error":
                return snapshot1
                
            snapshot2 = self.get_snapshot_content(url, timestamp2)
            if snapshot2["status"] == "error":
                return snapshot2
                
            # Basic comparison (you might want to implement more sophisticated comparison)
            content1 = snapshot1["content"]
            content2 = snapshot2["content"]
            
            # Save comparison results
            filename = os.path.join(
                self.results_dir, 
                f"comparison_{url.replace('://', '_').replace('/', '_')}_{timestamp1}_vs_{timestamp2}.json"
            )
            
            comparison_result = {
                "url": url,
                "timestamp1": timestamp1,
                "timestamp2": timestamp2,
                "length_diff": len(content2) - len(content1),
                "identical": content1 == content2
            }
            
            with open(filename, 'w') as f:
                json.dump(comparison_result, f, indent=2)
                
            return {
                "status": "success",
                "comparison": comparison_result,
                "saved_to": filename
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_recent_changes(self, url: str, days: int = 30) -> Dict:
        """Get recent changes for a URL within specified number of days"""
        try:
            # Get all snapshots first
            result = self.get_snapshots(url)
            if result["status"] == "error":
                return result
                
            # Filter recent snapshots
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            recent_snapshots = [
                snapshot for snapshot in result["snapshots"]
                if int(snapshot["timestamp"][:8]) >= int(datetime.fromtimestamp(cutoff_date).strftime("%Y%m%d"))
            ]
            
            return {
                "status": "success",
                "recent_changes": recent_snapshots
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
