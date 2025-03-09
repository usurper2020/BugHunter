import unittest
import json
import os
from unittest.mock import patch, mock_open
from datetime import datetime
from collaboration_system import CollaborationSystem

class TestCollaborationSystem(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.collab = CollaborationSystem()
        self.test_message = {
            'sender': 'testuser',
            'recipient': 'teammate',
            'content': 'Test message content'
        }
        self.test_task = {
            'creator': 'testuser',
            'assignee': 'teammate',
            'title': 'Test task',
            'description': 'Test task description',
            'priority': 'high'
        }
        self.test_note = {
            'user': 'testuser',
            'title': 'Test note',
            'content': 'Test note content',
            'tags': ['test', 'documentation']
        }

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_send_message(self, mock_file):
        """Test sending messages"""
        result = self.collab.send_message(
            self.test_message['sender'],
            self.test_message['recipient'],
            self.test_message['content']
        )
        
        self.assertEqual(result['status'], 'success')
        mock_file.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    def test_get_messages(self, mock_file):
        """Test retrieving messages"""
        # Mock stored messages
        mock_messages = [
            {
                'id': '1',
                'sender': 'testuser',
                'recipient': 'teammate',
                'content': 'Test message',
                'timestamp': datetime.now().isoformat(),
                'read': False
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_messages)
        
        messages = self.collab.get_messages('testuser')
        
        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['sender'], 'testuser')

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_create_task(self, mock_file):
        """Test task creation"""
        result = self.collab.create_task(
            self.test_task['creator'],
            self.test_task['assignee'],
            self.test_task['title'],
            self.test_task['description'],
            self.test_task['priority']
        )
        
        self.assertEqual(result['status'], 'success')
        mock_file.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    def test_update_task_status(self, mock_file):
        """Test updating task status"""
        # Mock stored tasks
        mock_tasks = [
            {
                'id': 'task_1',
                'status': 'pending',
                'creator': 'testuser',
                'assignee': 'teammate'
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_tasks)
        
        result = self.collab.update_task_status('task_1', 'in_progress')
        
        self.assertEqual(result['status'], 'success')
        mock_file.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    def test_get_tasks(self, mock_file):
        """Test retrieving tasks"""
        # Mock stored tasks
        mock_tasks = [
            {
                'id': 'task_1',
                'creator': 'testuser',
                'assignee': 'teammate',
                'title': 'Test task',
                'status': 'pending'
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_tasks)
        
        tasks = self.collab.get_tasks('testuser')
        
        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['creator'], 'testuser')

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_add_note(self, mock_file):
        """Test adding notes"""
        result = self.collab.add_note(
            self.test_note['user'],
            self.test_note['title'],
            self.test_note['content'],
            self.test_note['tags']
        )
        
        self.assertEqual(result['status'], 'success')
        mock_file.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    def test_get_notes(self, mock_file):
        """Test retrieving notes"""
        # Mock stored notes
        mock_notes = [
            {
                'id': 'note_1',
                'user': 'testuser',
                'title': 'Test note',
                'content': 'Test content',
                'tags': ['test']
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_notes)
        
        notes = self.collab.get_notes('testuser')
        
        self.assertIsInstance(notes, list)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['user'], 'testuser')

    @patch('builtins.open', new_callable=mock_open)
    def test_search_notes(self, mock_file):
        """Test searching notes"""
        # Mock stored notes
        mock_notes = [
            {
                'id': 'note_1',
                'title': 'Test note',
                'content': 'Searchable content',
                'tags': ['test', 'search']
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_notes)
        
        results = self.collab.search_notes('searchable')
        
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertIn('searchable', results[0]['content'].lower())

    @patch('builtins.open', new_callable=mock_open)
    def test_share_note(self, mock_file):
        """Test note sharing"""
        # Mock stored notes
        mock_notes = [
            {
                'id': 'note_1',
                'user': 'testuser',
                'shared_with': []
            }
        ]
        mock_file.return_value.read.return_value = json.dumps(mock_notes)
        
        result = self.collab.share_note('note_1', 'teammate')
        
        self.assertEqual(result['status'], 'success')
        mock_file.assert_called()

    def test_data_directory_creation(self):
        """Test collaboration directory creation"""
        # Delete directory if it exists
        if os.path.exists('data'):
            for file in ['messages.json', 'tasks.json', 'notes.json']:
                file_path = os.path.join('data', file)
                if os.path.exists(file_path):
                    os.remove(file_path)
            os.rmdir('data')
        
        # Create new instance to trigger directory creation
        collab = CollaborationSystem()
        
        self.assertTrue(os.path.exists('data'))
        self.assertTrue(os.path.exists(collab.messages_file))
        self.assertTrue(os.path.exists(collab.tasks_file))
        self.assertTrue(os.path.exists(collab.notes_file))

    def test_invalid_message(self):
        """Test sending invalid message"""
        result = self.collab.send_message('', '', '')
        self.assertEqual(result['status'], 'error')

    def test_invalid_task(self):
        """Test creating invalid task"""
        result = self.collab.create_task('', '', '', '')
        self.assertEqual(result['status'], 'error')

    def test_invalid_note(self):
        """Test creating invalid note"""
        result = self.collab.add_note('', '', '')
        self.assertEqual(result['status'], 'error')

if __name__ == '__main__':
    unittest.main()
