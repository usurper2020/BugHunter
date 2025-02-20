import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
from collections import defaultdict

class AnalyticsSystem:
    """
    Class for managing analytics monitoring within the BugHunter application.
    
    This class handles the monitoring of system analytics and provides
    status information about the monitoring system.
    """
    
    def __init__(self):
        """
        Initialize the AnalyticsSystem instance.
        
        Sets the monitoring state to False, indicating that the analytics
        monitoring system starts in a stopped state.
        """
        self.monitoring = False
        
    def start_monitoring(self):
        """
        Start the analytics monitoring system.
        
        Activates the monitoring system to begin collecting analytics
        data about system usage and performance.
        """
        self.monitoring = True
        
    def get_status(self):
        """
        Retrieve the current status of the analytics monitoring system.
        
        Returns:
            dict: A dictionary containing the monitoring state and the
            current operational status ('running' or 'stopped').
        """
        return {
            'monitoring': self.monitoring,
            'status': 'running' if self.monitoring else 'stopped'
        }
    """Manages security analytics and reporting"""
    
    def __init__(self):
        self.data_dir = os.path.join('data', 'analytics')
        self.reports_dir = os.path.join(self.data_dir, 'reports')
        self.graphs_dir = os.path.join(self.data_dir, 'graphs')
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.graphs_dir, exist_ok=True)
        
    def track_event(
        self,
        event_type: str,
        data: Dict,
        timestamp: Optional[datetime] = None
    ) -> Dict:
        """Track an analytics event"""
        try:
            timestamp = timestamp or datetime.now()
            event = {
                "type": event_type,
                "timestamp": str(timestamp),
                "data": data
            }
            
            # Save event to file
            filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{event_type}.json"
            with open(os.path.join(self.data_dir, filename), 'w') as f:
                json.dump(event, f, indent=2)
                
            return {
                "status": "success",
                "message": "Event tracked successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def generate_report(
        self,
        start_date: datetime,
        end_date: datetime,
        event_types: Optional[List[str]] = None
    ) -> Dict:
        """Generate an analytics report"""
        try:
            events = self._load_events(start_date, end_date, event_types)
            
            # Process events
            summary = self._generate_summary(events)
            trends = self._analyze_trends(events)
            
            report = {
                "period": {
                    "start": str(start_date),
                    "end": str(end_date)
                },
                "summary": summary,
                "trends": trends,
                "generated_at": str(datetime.now())
            }
            
            # Save report
            filename = f"report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.json"
            with open(os.path.join(self.reports_dir, filename), 'w') as f:
                json.dump(report, f, indent=2)
                
            return {
                "status": "success",
                "report": report,
                "file": filename
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def generate_graphs(
        self,
        start_date: datetime,
        end_date: datetime,
        event_types: Optional[List[str]] = None
    ) -> Dict:
        """Generate analytics graphs"""
        try:
            events = self._load_events(start_date, end_date, event_types)
            
            # Generate various graphs
            graphs = []
            
            # Event frequency over time
            time_graph = self._generate_time_graph(events)
            graphs.append(time_graph)
            
            # Event type distribution
            type_graph = self._generate_type_graph(events)
            graphs.append(type_graph)
            
            return {
                "status": "success",
                "graphs": graphs
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_statistics(
        self,
        period: str = "day"
    ) -> Dict:
        """Get current statistics"""
        try:
            end_date = datetime.now()
            if period == "day":
                start_date = end_date - timedelta(days=1)
            elif period == "week":
                start_date = end_date - timedelta(weeks=1)
            elif period == "month":
                start_date = end_date - timedelta(days=30)
            else:
                return {
                    "status": "error",
                    "message": "Invalid period specified"
                }
                
            events = self._load_events(start_date, end_date)
            stats = self._calculate_statistics(events)
            
            return {
                "status": "success",
                "statistics": stats
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _load_events(
        self,
        start_date: datetime,
        end_date: datetime,
        event_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """Load events within the specified period"""
        events = []
        for filename in os.listdir(self.data_dir):
            if not filename.endswith('.json'):
                continue
                
            with open(os.path.join(self.data_dir, filename)) as f:
                event = json.load(f)
                
            event_time = datetime.fromisoformat(event['timestamp'])
            if event_time < start_date or event_time > end_date:
                continue
                
            if event_types and event['type'] not in event_types:
                continue
                
            events.append(event)
            
        return sorted(events, key=lambda x: x['timestamp'])
        
    def _generate_summary(self, events: List[Dict]) -> Dict:
        """Generate a summary of events"""
        summary = {
            "total_events": len(events),
            "event_types": defaultdict(int),
            "unique_users": set()
        }
        
        for event in events:
            summary["event_types"][event["type"]] += 1
            if "user" in event["data"]:
                summary["unique_users"].add(event["data"]["user"])
                
        summary["unique_users"] = len(summary["unique_users"])
        return summary
        
    def _analyze_trends(self, events: List[Dict]) -> Dict:
        """Analyze trends in events"""
        if not events:
            return {}
            
        # Group events by day
        daily_counts = defaultdict(lambda: defaultdict(int))
        for event in events:
            date = datetime.fromisoformat(event['timestamp']).date()
            daily_counts[date][event['type']] += 1
            
        # Calculate trends
        trends = {
            "daily_activity": dict(daily_counts),
            "peak_day": max(daily_counts.items(), key=lambda x: sum(x[1].values()))[0].isoformat()
        }
        
        return trends
        
    def _generate_time_graph(self, events: List[Dict]) -> str:
        """Generate time-based frequency graph"""
        if not events:
            return ""
            
        dates = [datetime.fromisoformat(e['timestamp']).date() for e in events]
        counts = defaultdict(int)
        for date in dates:
            counts[date] += 1
            
        plt.figure(figsize=(12, 6))
        plt.plot(list(counts.keys()), list(counts.values()))
        plt.title("Event Frequency Over Time")
        plt.xlabel("Date")
        plt.ylabel("Number of Events")
        plt.xticks(rotation=45)
        
        filename = f"time_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.graphs_dir, filename)
        plt.savefig(filepath)
        plt.close()
        
        return filepath
        
    def _generate_type_graph(self, events: List[Dict]) -> str:
        """Generate event type distribution graph"""
        if not events:
            return ""
            
        type_counts = defaultdict(int)
        for event in events:
            type_counts[event['type']] += 1
            
        plt.figure(figsize=(10, 10))
        plt.pie(
            list(type_counts.values()),
            labels=list(type_counts.keys()),
            autopct='%1.1f%%'
        )
        plt.title("Event Type Distribution")
        
        filename = f"type_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.graphs_dir, filename)
        plt.savefig(filepath)
        plt.close()
        
        return filepath
        
    def _calculate_statistics(self, events: List[Dict]) -> Dict:
        """Calculate various statistics from events"""
        if not events:
            return {}
            
        stats = {
            "total_events": len(events),
            "event_types": defaultdict(int),
            "hourly_distribution": defaultdict(int),
            "user_activity": defaultdict(int)
        }
        
        for event in events:
            event_time = datetime.fromisoformat(event['timestamp'])
            stats["event_types"][event["type"]] += 1
            stats["hourly_distribution"][event_time.hour] += 1
            if "user" in event["data"]:
                stats["user_activity"][event["data"]["user"]] += 1
                
        return stats
