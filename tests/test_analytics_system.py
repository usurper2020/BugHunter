import unittest
import json
import os
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta
from analytics_system import AnalyticsSystem

class TestAnalyticsSystem(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.analytics = AnalyticsSystem()
        self.test_scan = {
            'timestamp': datetime.now().isoformat(),
            'user': 'testuser',
            'target': 'http://example.com',
            'findings': [
                {
                    'type': 'sql_injection',
                    'severity': 'high',
                    'description': 'SQL Injection vulnerability',
                    'details': 'Parameter vulnerable to SQL injection'
                },
                {
                    'type': 'xss',
                    'severity': 'medium',
                    'description': 'Cross-site scripting vulnerability',
                    'details': 'Reflected XSS in search parameter'
                }
            ]
        }

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_record_scan(self, mock_file):
        """Test recording scan data"""
        result = self.analytics.record_scan(
            self.test_scan['user'],
            self.test_scan['target'],
            self.test_scan['findings']
        )
        
        self.assertEqual(result['status'], 'success')
        mock_file.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    def test_get_scan_stats(self, mock_file):
        """Test retrieving scan statistics"""
        # Mock stored scan data
        mock_scans = [
            {
                'timestamp': (datetime.now() - timedelta(days=1)).isoformat(),
                'user': 'testuser',
                'target': 'http://example.com',
                'finding_count': 2,
                'severity_counts': {'high': 1, 'medium': 1}
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_scans)
        
        stats = self.analytics.get_scan_stats(days=7)
        
        self.assertIn('total_scans', stats)
        self.assertIn('total_findings', stats)
        self.assertIn('severity_distribution', stats)
        self.assertIn('scans_per_day', stats)

    @patch('builtins.open', new_callable=mock_open)
    def test_vulnerability_trends(self, mock_file):
        """Test vulnerability trend analysis"""
        # Mock vulnerability data
        mock_vulns = [
            {
                'timestamp': (datetime.now() - timedelta(days=1)).isoformat(),
                'type': 'sql_injection',
                'severity': 'high',
                'target': 'http://example.com'
            },
            {
                'timestamp': datetime.now().isoformat(),
                'type': 'xss',
                'severity': 'medium',
                'target': 'http://example.com'
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_vulns)
        
        trends = self.analytics.get_vulnerability_trends(days=7)
        
        self.assertIn('type_distribution', trends)
        self.assertIn('severity_distribution', trends)
        self.assertIn('daily_counts', trends)

    @patch('matplotlib.pyplot.savefig')
    def test_generate_charts(self, mock_savefig):
        """Test chart generation"""
        # Mock the BytesIO and base64 encoding
        mock_buffer = MagicMock()
        mock_buffer.getvalue.return_value = b'mock_image_data'
        
        with patch('io.BytesIO', return_value=mock_buffer):
            charts = self.analytics.generate_charts()
            
            self.assertIn('severity_pie', charts)
            self.assertIn('daily_scans', charts)
            self.assertIn('vuln_types', charts)
            mock_savefig.assert_called()

    def test_data_directory_creation(self):
        """Test analytics directory creation"""
        # Delete directory if it exists
        if os.path.exists(self.analytics.analytics_dir):
            os.rmdir(self.analytics.analytics_dir)
        
        # Create new instance to trigger directory creation
        analytics = AnalyticsSystem()
        
        self.assertTrue(os.path.exists(analytics.analytics_dir))
        self.assertTrue(os.path.exists(analytics.scan_stats_file))
        self.assertTrue(os.path.exists(analytics.vuln_stats_file))
        self.assertTrue(os.path.exists(analytics.user_stats_file))

    @patch('builtins.open', new_callable=mock_open)
    def test_user_performance(self, mock_file):
        """Test user performance statistics"""
        # Mock user statistics data
        mock_stats = {
            'testuser': {
                'scans': 10,
                'findings': 25,
                'reports': 8
            },
            'admin': {
                'scans': 15,
                'findings': 30,
                'reports': 12
            }
        }
        mock_file.return_value.read.return_value = json.dumps(mock_stats)
        
        performance = self.analytics.get_user_performance()
        
        self.assertIsInstance(performance, dict)
        self.assertIn('testuser', performance)
        self.assertIn('admin', performance)
        for user_stats in performance.values():
            self.assertIn('scans', user_stats)
            self.assertIn('findings', user_stats)
            self.assertIn('reports', user_stats)

    def test_invalid_date_range(self):
        """Test analytics with invalid date range"""
        stats = self.analytics.get_scan_stats(days=-1)
        self.assertIn('error', stats)
        
        trends = self.analytics.get_vulnerability_trends(days=0)
        self.assertIn('error', trends)

    @patch('builtins.open', new_callable=mock_open)
    def test_daily_scan_calculation(self, mock_file):
        """Test daily scan count calculation"""
        # Mock scan data for multiple days
        today = datetime.now()
        mock_scans = [
            {
                'timestamp': today.isoformat(),
                'finding_count': 2,
                'severity_counts': {'high': 1, 'medium': 1}
            },
            {
                'timestamp': (today - timedelta(days=1)).isoformat(),
                'finding_count': 3,
                'severity_counts': {'high': 2, 'low': 1}
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_scans)
        
        stats = self.analytics.get_scan_stats(days=7)
        daily_scans = stats['scans_per_day']
        
        self.assertIsInstance(daily_scans, dict)
        self.assertEqual(len(daily_scans), 2)  # Two days of data
        self.assertEqual(sum(daily_scans.values()), len(mock_scans))

if __name__ == '__main__':
    unittest.main()
