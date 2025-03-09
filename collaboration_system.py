import json
import time
from datetime import datetime
import os
from queue import Queue
from threading import Lock

class CollaborationSystem:
    def __init__(self):
        self.messages_file = 'data/messages.json'
        self.tasks_file = 'data/tasks.json'
        self.notes_file = 'data/notes.json'
        self.message_queue = Queue()
        self.lock = Lock()
        self.create_data_directory()

    def create_data_directory(self):
        """Create the data directory and required files if they don't exist"""
        os.makedirs('data', exist_ok=True)
        
        # Initialize messages file
        if not os.path.exists(self.messages_file):
            with open(self.messages_file, 'w') as f:
                json.dump([], f)
        
        # Initialize tasks file
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w') as f:
                json.dump([], f)
        
        # Initialize notes file
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, 'w') as f:
                json.dump([], f)

    def send_message(self, sender, recipient, content):
        """Send a message to another user"""
        message = {
            'id': str(time.time()),
            'sender': sender,
            'recipient': recipient,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        
        with self.lock:
            try:
                with open(self.messages_file, 'r') as f:
                    messages = json.load(f)
                messages.append(message)
                with open(self.messages_file, 'w') as f:
                    json.dump(messages, f)
                return {'status': 'success', 'message': 'Message sent successfully'}
            except Exception as e:
                return {'status': 'error', 'message': f'Failed to send message: {str(e)}'}

    def get_messages(self, user):
        """Get all messages for a user"""
        try:
            with open(self.messages_file, 'r') as f:
                messages = json.load(f)
            return [m for m in messages if m['recipient'] == user or m['sender'] == user]
        except Exception as e:
            return []

    def create_task(self, creator, assignee, title, description, priority='medium'):
        """Create a new task"""
        task = {
            'id': str(time.time()),
            'creator': creator,
            'assignee': assignee,
            'title': title,
            'description': description,
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        with self.lock:
            try:
                with open(self.tasks_file, 'r') as f:
                    tasks = json.load(f)
                tasks.append(task)
                with open(self.tasks_file, 'w') as f:
                    json.dump(tasks, f)
                return {'status': 'success', 'message': 'Task created successfully'}
            except Exception as e:
                return {'status': 'error', 'message': f'Failed to create task: {str(e)}'}

    def update_task_status(self, task_id, new_status):
        """Update the status of a task"""
        with self.lock:
            try:
                with open(self.tasks_file, 'r') as f:
                    tasks = json.load(f)
                
                for task in tasks:
                    if task['id'] == task_id:
                        task['status'] = new_status
                        task['updated_at'] = datetime.now().isoformat()
                        break
                
                with open(self.tasks_file, 'w') as f:
                    json.dump(tasks, f)
                return {'status': 'success', 'message': 'Task status updated successfully'}
            except Exception as e:
                return {'status': 'error', 'message': f'Failed to update task status: {str(e)}'}

    def get_tasks(self, user=None):
        """Get tasks, optionally filtered by user"""
        try:
            with open(self.tasks_file, 'r') as f:
                tasks = json.load(f)
            if user:
                return [t for t in tasks if t['assignee'] == user or t['creator'] == user]
            return tasks
        except Exception as e:
            return []

    def add_note(self, user, title, content, tags=None):
        """Add a new note"""
        note = {
            'id': str(time.time()),
            'user': user,
            'title': title,
            'content': content,
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        with self.lock:
            try:
                with open(self.notes_file, 'r') as f:
                    notes = json.load(f)
                notes.append(note)
                with open(self.notes_file, 'w') as f:
                    json.dump(notes, f)
                return {'status': 'success', 'message': 'Note added successfully'}
            except Exception as e:
                return {'status': 'error', 'message': f'Failed to add note: {str(e)}'}

    def get_notes(self, user=None, tag=None):
        """Get notes, optionally filtered by user and/or tag"""
        try:
            with open(self.notes_file, 'r') as f:
                notes = json.load(f)
            
            filtered_notes = notes
            if user:
                filtered_notes = [n for n in filtered_notes if n['user'] == user]
            if tag:
                filtered_notes = [n for n in filtered_notes if tag in n['tags']]
            
            return filtered_notes
        except Exception as e:
            return []

    def search_notes(self, query):
        """Search notes by content"""
        try:
            with open(self.notes_file, 'r') as f:
                notes = json.load(f)
            return [n for n in notes if query.lower() in n['content'].lower() or 
                   query.lower() in n['title'].lower() or 
                   any(query.lower() in tag.lower() for tag in n['tags'])]
        except Exception as e:
            return []

    def share_note(self, note_id, shared_with):
        """Share a note with another user"""
        with self.lock:
            try:
                with open(self.notes_file, 'r') as f:
                    notes = json.load(f)
                
                for note in notes:
                    if note['id'] == note_id:
                        if 'shared_with' not in note:
                            note['shared_with'] = []
                        if shared_with not in note['shared_with']:
                            note['shared_with'].append(shared_with)
                        break
                
                with open(self.notes_file, 'w') as f:
                    json.dump(notes, f)
                return {'status': 'success', 'message': 'Note shared successfully'}
            except Exception as e:
                return {'status': 'error', 'message': f'Failed to share note: {str(e)}'}
