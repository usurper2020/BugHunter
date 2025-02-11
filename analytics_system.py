import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class AnalyticsSystem:
    def __init__(self):
        self.analytics_dir = 'data/analytics'
        self.scan_stats_file = f'{self.analytics_dir}/scan_stats.json'
        self.vuln_stats_file = f'{self.analytics_dir}/vulnerability_stats.json'
        self.user_stats_file = f'{self.analytics_dir}/user_stats.json'
        self.create_analytics_directory()

    def create_analytics_directory(self):
        """Create analytics directory and initialize files if they don't exist"""
        os.makedirs(self.analytics_dir, exist_ok=True)
        
        # Initialize scan stats file
        if not os.path.exists(self.scan_stats_file):
            with open(self.scan_stats_file, 'w') as f:
                json.dump([], f)
        
        # Initialize vulnerability stats file
        if not os.path.exists(self.vuln_stats_file):
            with open(self.vuln_stats_file, 'w') as f:
                json.dump([], f)
        
        # Initialize user stats file
        if not os.path.exists(self.user_stats_file):
            with open(self.user_stats_file, 'w') as f:
                json.dump({}, f)

    def record_scan(self, user, target, findings):
        """Record a scan and its findings"""
        scan_record = {
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'target': target,
            'finding_count': len(findings),
            'severity_counts': self._count_severities(findings)
        }
        
        try:
            with open(self.scan_stats_file, 'r') as f:
                scans = json.load(f)
            scans.append(scan_record)
            with open(self.scan_stats_file, 'w') as f:
                json.dump(scans, f)
            
            self._update_user_stats(user, 'scans')
            return {'status': 'success', 'message': 'Scan recorded successfully'}
        except Exception as e:
            return {'status': 'error', 'message': f'Failed to record scan: {str(e)}'}

    def record_vulnerability(self, vulnerability_type, severity, target):
        """Record a found vulnerability"""
        vuln_record = {
            'timestamp': datetime.now().isoformat(),
            'type': vulnerability_type,
            'severity': severity,
            'target': target
        }
        
        try:
            with open(self.vuln_stats_file, 'r') as f:
                vulns = json.load(f)
            vulns.append(vuln_record)
            with open(self.vuln_stats_file, 'w') as f:
                json.dump(vulns, f)
            return {'status': 'success', 'message': 'Vulnerability recorded successfully'}
        except Exception as e:
            return {'status': 'error', 'message': f'Failed to record vulnerability: {str(e)}'}

    def _update_user_stats(self, username, activity_type):
        """Update user activity statistics"""
        try:
            with open(self.user_stats_file, 'r') as f:
                user_stats = json.load(f)
            
            if username not in user_stats:
                user_stats[username] = {'scans': 0, 'findings': 0, 'reports': 0}
            
            user_stats[username][activity_type] = user_stats[username].get(activity_type, 0) + 1
            
            with open(self.user_stats_file, 'w') as f:
                json.dump(user_stats, f)
        except Exception:
            pass  # Silently fail for stats updates

    def _count_severities(self, findings):
        """Count findings by severity"""
        severity_counts = defaultdict(int)
        for finding in findings:
            severity_counts[finding['severity']] += 1
        return dict(severity_counts)

    def get_scan_stats(self, days=30):
        """Get scan statistics for the specified number of days"""
        try:
            with open(self.scan_stats_file, 'r') as f:
                scans = json.load(f)
            
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_scans = [
                scan for scan in scans 
                if datetime.fromisoformat(scan['timestamp']) > cutoff_date
            ]
            
            total_scans = len(recent_scans)
            total_findings = sum(scan['finding_count'] for scan in recent_scans)
            severity_counts = defaultdict(int)
            for scan in recent_scans:
                for severity, count in scan['severity_counts'].items():
                    severity_counts[severity] += count
            
            return {
                'total_scans': total_scans,
                'total_findings': total_findings,
                'severity_distribution': dict(severity_counts),
                'scans_per_day': self._calculate_daily_scans(recent_scans)
            }
        except Exception as e:
            return {'error': str(e)}

    def get_vulnerability_trends(self, days=30):
        """Get vulnerability trends for the specified number of days"""
        try:
            with open(self.vuln_stats_file, 'r') as f:
                vulns = json.load(f)
            
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_vulns = [
                vuln for vuln in vulns 
                if datetime.fromisoformat(vuln['timestamp']) > cutoff_date
            ]
            
            type_counts = defaultdict(int)
            severity_counts = defaultdict(int)
            daily_counts = defaultdict(int)
            
            for vuln in recent_vulns:
                type_counts[vuln['type']] += 1
                severity_counts[vuln['severity']] += 1
                date = datetime.fromisoformat(vuln['timestamp']).date()
                daily_counts[date.isoformat()] += 1
            
            return {
                'type_distribution': dict(type_counts),
                'severity_distribution': dict(severity_counts),
                'daily_counts': dict(daily_counts)
            }
        except Exception as e:
            return {'error': str(e)}

    def get_user_performance(self):
        """Get user performance statistics"""
        try:
            with open(self.user_stats_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {'error': str(e)}

    def _calculate_daily_scans(self, scans):
        """Calculate the number of scans per day"""
        daily_counts = defaultdict(int)
        for scan in scans:
            date = datetime.fromisoformat(scan['timestamp']).date()
            daily_counts[date.isoformat()] += 1
        return dict(daily_counts)

    def generate_charts(self):
        """Generate charts for the dashboard"""
        charts = {}
        
        # Get statistics
        scan_stats = self.get_scan_stats()
        vuln_trends = self.get_vulnerability_trends()
        
        if 'error' not in scan_stats and 'error' not in vuln_trends:
            # Severity Distribution Pie Chart
            plt.figure(figsize=(8, 6))
            plt.pie(scan_stats['severity_distribution'].values(),
                   labels=scan_stats['severity_distribution'].keys(),
                   autopct='%1.1f%%')
            plt.title('Vulnerability Severity Distribution')
            charts['severity_pie'] = self._get_plot_as_base64()
            
            # Daily Scans Line Chart
            plt.figure(figsize=(10, 6))
            dates = list(scan_stats['scans_per_day'].keys())
            counts = list(scan_stats['scans_per_day'].values())
            plt.plot(dates, counts)
            plt.title('Daily Scan Activity')
            plt.xticks(rotation=45)
            plt.tight_layout()
            charts['daily_scans'] = self._get_plot_as_base64()
            
            # Vulnerability Types Bar Chart
            plt.figure(figsize=(10, 6))
            types = list(vuln_trends['type_distribution'].keys())
            counts = list(vuln_trends['type_distribution'].values())
            plt.bar(types, counts)
            plt.title('Vulnerability Types Distribution')
            plt.xticks(rotation=45)
            plt.tight_layout()
            charts['vuln_types'] = self._get_plot_as_base64()
        
        return charts

    def _get_plot_as_base64(self):
        """Convert the current matplotlib plot to a base64 string"""
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()
        return image_base64
