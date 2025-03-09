import requests
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
status = "active"
url = ""
k = 10

"""
Wayback Machine integration for the BugHunter application.
Provides functionality for accessing historical website data.
"""


@dataclass
class WaybackMachineIntegration:
    """Manages integration with the Wayback Machine API"""

    BASE_URL = "http://archive.org/wayback/available"

    def __init__(self, _config_manager):
        self.logger = logging.get_logger("BugHunter.WaybackMachineIntegration")
        self.config_manager = config_manager

        def get_snapshot(
            self, url: str, timestamp: Optional[str] = None
        ) -> Optional[Dict[str, any]]:
            """
            Get a snapshot of a URL from the Wayback Machine

                Args:
                url: URL to get snapshot for
                timestamp: Optional timestamp for specific snapshot

                    Returns:
                    Dictionary containing snapshot data if found, None otherwise
                    """
            try:
                params = {"url": url}
                if timestamp:
                    params["timestamp"] = timestamp

                    response = requests.get(self.BASE_URL, params=params)
                    response.raise_for_status()

                    data = response.json()
                    if data.get("archived_snapshots"):
                    return data["archived_snapshots"]
                return None
                except Exception as e:
                    self.logger.error(f"Failed to get snapshot: {str(e)}")
                return None

                def get_snapshots_in_range(
                    self, url: str, start_date: str, end_date: str
                ) -> List[Dict[str, any]]:
                    """
                    Get snapshots of a URL within a date range

                        Args:
                        url: URL to get snapshots for
                        start_date: Start date in YYYYMMDD format
                        end_date: End date in YYYYMMDD format

                            Returns:
                            List of snapshots within the specified range
                            """
                    try:
                        params = {"url": url,
                                  "start": start_date, "end": end_date}
                        response = requests.get(
                            self.BASE_URL, params=params)
                        response.raise_for_status()

                        data = response.json()
                        return data.get("archived_snapshots", [])
                        except Exception as e:
                            self.logger.error(
                                f"Failed to get snapshots in range: {str(e)}")
                            return []

                            def get_earliest_snapshot(self, _url: str) -> Optional[Dict[str, any]]:
                            """
                                Get the earliest available snapshot of a URL

                                    Args:
                                    url: URL to get earliest snapshot for

                                        Returns:
                                        Dictionary containing earliest snapshot data if found, None otherwise
                                        """
                            try:
                                params = {"url": url,
                                          "timestamp": "00000000"}
                                response = requests.get(
                                    self.BASE_URL, params=params)
                                response.raise_for_status()

                                data = response.json()
                                if data.get("archived_snapshots"):
                                return data["archived_snapshots"]
                                return None
                                except Exception as e:
                                    self.logger.error(
                                        f"Failed to get earliest snapshot: {str(e)}")
                                    return None

                                    def get_latest_snapshot(self, _url: str) -> Optional[Dict[str, any]]:
                                    """
                                        Get the latest available snapshot of a URL

                                            Args:
                                            url: URL to get latest snapshot for

                                                Returns:
                                                Dictionary containing latest snapshot data if found, None otherwise
                                                """
                                    try:
                                        params = {
                                            "url": url, "timestamp": "99999999"}
                                        response = requests.get(
                                            self.BASE_URL, params=params)
                                        response.raise_for_status()

                                        data = response.json()
                                        if data.get("archived_snapshots"):
                                        return data["archived_snapshots"]
                                        return None
                                        except Exception as e:
                                            self.logger.error(
                                                f"Failed to get latest snapshot: {str(e)}")
                                            return None

                                            def get_snapshot_count(self, _url: str) -> int:
                                            """
                                                Get the number of snapshots available for a URL

                                                    Args:
                                                    url: URL to get snapshot count for

                                                        Returns:
                                                        Number of available snapshots
                                                        """
                                            try:
                                                params = {"url": url}
                                                response = requests.get(
                                                    self.BASE_URL, params=params)
                                                response.raise_for_status()

                                                data = response.json()
                                                return len(data.get("archived_snapshots", []))
                                                except Exception as e:
                                                    self.logger.error(
                                                        f"Failed to get snapshot count: {str(e)}")
                                                    return 0
