import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime
from contribution_system import ContributionSystem

class TestContributionSystem(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.contrib = ContributionSystem()
        self.test_contribution = {
            'username': 'testuser',
            'tool_name': 'TestTool',
            'tool_description': 'A test security tool',
            'tool_file': 'test_tool.py'
        }

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_submit_contribution(self, mock_file):
        """Test submitting a new tool contribution"""
        result = self.contrib.submit_contribution(
            self.test_contribution['username'],
            self.test_contribution['tool_name'],
            self.test_contribution['tool_description'],
            self.test_contribution['tool_file']
        )
        
        self.assertEqual(result['status'], 'success')
        mock_file.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    def test_get_contributions(self, mock_file):
        """Test retrieving contributions"""
        # Mock stored contributions
        mock_contributions = [
            {
                'id': str(datetime.now().timestamp()),
                'username': 'testuser',
                'tool_name': 'TestTool',
                'description': 'A test security tool',
                'file': 'test_tool.py',
                'submitted_at': datetime.now().isoformat()
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_contributions)
        
        contributions = self.contrib.get_contributions()
        
        self.assertIsInstance(contributions, list)
        self.assertEqual(len(contributions), 1)
        self.assertEqual(contributions[0]['username'], 'testuser')

    @patch('builtins.open', new_callable=mock_open)
    def test_delete_contribution(self, mock_file):
        """Test deleting a contribution"""
        contribution_id = 'test_id_123'
        # Mock stored contributions
        mock_contributions = [
            {
                'id': contribution_id,
                'username': 'testuser',
                'tool_name': 'TestTool'
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_contributions)
        
        result = self.contrib.delete_contribution(contribution_id)
        
        self.assertEqual(result['status'], 'success')
        mock_file.assert_called()

    def test_invalid_submission(self):
        """Test submitting invalid contribution"""
        # Test with empty values
        result = self.contrib.submit_contribution('', '', '', '')
        self.assertEqual(result['status'], 'error')
        self.assertIn('failed', result['message'].lower())

    def test_data_directory_creation(self):
        """Test contributions directory creation"""
        # Delete directory if it exists
        if os.path.exists('data'):
            if os.path.exists(self.contrib.contributions_file):
                os.remove(self.contrib.contributions_file)
            os.rmdir('data')
        
        # Create new instance to trigger directory creation
        contrib = ContributionSystem()
        
        self.assertTrue(os.path.exists('data'))
        self.assertTrue(os.path.exists(contrib.contributions_file))

    @patch('builtins.open', new_callable=mock_open)
    def test_duplicate_tool_name(self, mock_file):
        """Test submitting tool with existing name"""
        # Mock existing contributions
        mock_contributions = [
            {
                'id': 'existing_id',
                'tool_name': 'TestTool',
                'username': 'otheruser'
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_contributions)
        
        result = self.contrib.submit_contribution(
            'testuser',
            'TestTool',  # Same name as existing tool
            'Another test tool',
            'test_tool.py'
        )
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('exists', result['message'].lower())

    @patch('builtins.open', new_callable=mock_open)
    def test_contribution_validation(self, mock_file):
        """Test contribution data validation"""
        invalid_contributions = [
            {
                'username': 'testuser',
                'tool_name': '',  # Empty tool name
                'tool_description': 'Test description',
                'tool_file': 'test.py'
            },
            {
                'username': 'testuser',
                'tool_name': 'TestTool',
                'tool_description': '',  # Empty description
                'tool_file': 'test.py'
            },
            {
                'username': 'testuser',
                'tool_name': 'TestTool',
                'tool_description': 'Test description',
                'tool_file': ''  # Empty file path
            }
        ]
        
        for invalid_contrib in invalid_contributions:
            result = self.contrib.submit_contribution(
                invalid_contrib['username'],
                invalid_contrib['tool_name'],
                invalid_contrib['tool_description'],
                invalid_contrib['tool_file']
            )
            self.assertEqual(result['status'], 'error')

    @patch('builtins.open', new_callable=mock_open)
    def test_nonexistent_contribution_deletion(self, mock_file):
        """Test deleting non-existent contribution"""
        # Mock empty contributions list
        mock_file.return_value.read.return_value = '[]'
        
        result = self.contrib.delete_contribution('nonexistent_id')
        
        self.assertEqual(result['status'], 'error')
        self.assertIn('not found', result['message'].lower())

    def test_file_operations(self):
        """Test file operation error handling"""
        # Test with invalid file path
        with patch('builtins.open', side_effect=IOError):
            result = self.contrib.get_contributions()
            self.assertEqual(result, [])
            
            result = self.contrib.submit_contribution(
                'testuser',
                'TestTool',
                'Test description',
                'test.py'
            )
            self.assertEqual(result['status'], 'error')

if __name__ == '__main__':
    unittest.main()
