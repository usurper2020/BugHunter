import unittest
import os
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
from report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.report_gen = ReportGenerator()
        self.test_scan_results = {
            'id': 'scan_001',
            'target': 'http://example.com',
            'timestamp': datetime.now().isoformat(),
            'findings': [
                {
                    'type': 'sql_injection',
                    'severity': 'critical',
                    'description': 'SQL Injection vulnerability',
                    'details': 'Parameter vulnerable to SQL injection'
                },
                {
                    'type': 'xss',
                    'severity': 'high',
                    'description': 'Cross-site scripting vulnerability',
                    'details': 'Reflected XSS in search parameter'
                }
            ]
        }

    def test_directory_creation(self):
        """Test reports directory creation"""
        # Delete directory if it exists
        if os.path.exists(self.report_gen.reports_directory):
            os.rmdir(self.report_gen.reports_directory)
        
        # Create new instance to trigger directory creation
        report_gen = ReportGenerator()
        
        self.assertTrue(os.path.exists(report_gen.reports_directory))

    @patch('fpdf.FPDF')
    def test_generate_pdf_report(self, mock_fpdf):
        """Test PDF report generation"""
        # Mock FPDF instance
        mock_pdf = MagicMock()
        mock_fpdf.return_value = mock_pdf
        
        filename = self.report_gen.generate_report(self.test_scan_results, format='pdf')
        
        self.assertTrue(filename.endswith('.pdf'))
        mock_pdf.output.assert_called_once()

    def test_generate_json_report(self):
        """Test JSON report generation"""
        with patch('builtins.open', mock_open()) as mock_file:
            filename = self.report_gen.generate_report(self.test_scan_results, format='json')
            
            self.assertTrue(filename.endswith('.json'))
            mock_file.assert_called_once()

    def test_generate_html_report(self):
        """Test HTML report generation"""
        with patch('builtins.open', mock_open()) as mock_file:
            filename = self.report_gen.generate_report(self.test_scan_results, format='html')
            
            self.assertTrue(filename.endswith('.html'))
            mock_file.assert_called_once()

    def test_invalid_format(self):
        """Test report generation with invalid format"""
        with self.assertRaises(ValueError):
            self.report_gen.generate_report(self.test_scan_results, format='invalid')

    def test_empty_results(self):
        """Test report generation with empty results"""
        empty_results = {
            'id': 'scan_002',
            'target': 'http://example.com',
            'timestamp': datetime.now().isoformat(),
            'findings': []
        }
        
        with patch('builtins.open', mock_open()):
            filename = self.report_gen.generate_report(empty_results, format='pdf')
            self.assertIsNotNone(filename)

    @patch('fpdf.FPDF')
    def test_pdf_content(self, mock_fpdf):
        """Test PDF report content"""
        # Mock FPDF instance
        mock_pdf = MagicMock()
        mock_fpdf.return_value = mock_pdf
        
        self.report_gen.generate_report(self.test_scan_results, format='pdf')
        
        # Verify title and content were added
        mock_pdf.cell.assert_called()
        mock_pdf.add_page.assert_called_once()

    def test_html_content(self):
        """Test HTML report content"""
        with patch('builtins.open', mock_open()) as mock_file:
            self.report_gen.generate_report(self.test_scan_results, format='html')
            
            # Get the content written to the file
            written_content = ''
            for call in mock_file().write.call_args_list:
                written_content += call[0][0]
            
            # Check for essential HTML elements
            self.assertIn('<!DOCTYPE html>', written_content)
            self.assertIn('</html>', written_content)
            self.assertIn(self.test_scan_results['target'], written_content)
            self.assertIn('sql_injection', written_content)
            self.assertIn('xss', written_content)

    def test_json_content(self):
        """Test JSON report content"""
        with patch('builtins.open', mock_open()) as mock_file:
            self.report_gen.generate_report(self.test_scan_results, format='json')
            
            # Verify json.dump was called with correct data
            mock_file().write.assert_called()

    def test_report_filename(self):
        """Test report filename generation"""
        with patch('builtins.open', mock_open()):
            filename = self.report_gen.generate_report(self.test_scan_results, format='pdf')
            
            # Check filename format
            self.assertRegex(filename, r'report_\d{8}_\d{6}\.pdf')

    @patch('os.path.exists')
    def test_duplicate_filename_handling(self, mock_exists):
        """Test handling of duplicate filenames"""
        # Mock that the file already exists, then doesn't exist
        mock_exists.side_effect = [True, False]
        
        with patch('builtins.open', mock_open()):
            filename = self.report_gen.generate_report(self.test_scan_results, format='pdf')
            
            # Should have appended a number to the filename
            self.assertRegex(filename, r'report_\d{8}_\d{6}_\d+\.pdf')

    def test_file_operation_errors(self):
        """Test handling of file operation errors"""
        with patch('builtins.open', side_effect=IOError):
            with self.assertRaises(Exception):
                self.report_gen.generate_report(self.test_scan_results, format='pdf')

if __name__ == '__main__':
    unittest.main()
