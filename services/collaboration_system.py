import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from collaboration_dialog import CollaborationDialog
from collaboration import Collaboration
from contribution_dialog import ContributionDialog
from contribution_system import ContributionSystem
from notification import NotificationSystem

class CollaborationSystem:
    """
    Class for managing collaboration features within the BugHunter application.
    
    This class provides functionality for:
    - Message management between users
    - Task creation and tracking
    - Note sharing and organization
    - File-based data persistence
    - Thread-safe operations
    """
    
    def __init__(self):
        """
        Initialize the CollaborationSystem instance.
        
        Sets up:
        - File paths for messages, tasks, and notes storage
        - Message queue for asynchronous processing
        - Thread lock for safe concurrent access
        - Data directory and required files
        """
        self.messages_file = 'data/messages.json'
        self.tasks_file = 'data/tasks.json'
        self.notes_file = 'data/notes.json'
        self.message_queue = Queue()
        self.lock = Lock()
        self.create_data_directory()

    def create_data_directory(self):
        """
        Create the data directory and initialize required JSON files.
        
        Creates:
        - data/ directory if it doesn't exist
        - messages.json for storing user messages
        - tasks.json for storing task information
        - notes.json for storing user notes
        
        Each file is initialized with an empty array if it doesn't exist.
        """
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
        """
        Send a message from one user to another.
        
        Parameters:
            sender (str): The username of the message sender
            recipient (str): The username of the message recipient
            content (str): The content of the message
            
        Returns:
            dict: A status dictionary containing:
                - status: 'success' or 'error'
                - message: A description of the result
        
        Thread-safe: Uses lock to ensure safe file operations.
        """
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
        """
        Retrieve all messages for a specific user.
        
        Gets both sent and received messages for the specified user.
        
        Parameters:
            user (str): The username to get messages for
            
        Returns:
            list: A list of message dictionaries where the user is either
            the sender or recipient. Returns empty list on error.
        """
        try:
            with open(self.messages_file, 'r') as f:
                messages = json.load(f)
            return [m for m in messages if m['recipient'] == user or m['sender'] == user]
        except Exception as e:
            return []

    def create_task(self, creator, assignee, title, description, priority='medium'):
        """
        Create a new task in the system.
        
        Parameters:
            creator (str): Username of the task creator
            assignee (str): Username of the person assigned to the task
            title (str): Title of the task
            description (str): Detailed description of the task
            priority (str, optional): Task priority level. Defaults to 'medium'
            
        Returns:
            dict: A status dictionary containing:
                - status: 'success' or 'error'
                - message: A description of the result
                
        Thread-safe: Uses lock to ensure safe file operations.
        """
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
        """
        Update the status of an existing task.
        
        Parameters:
            task_id (str): The unique identifier of the task
            new_status (str): The new status to set for the task
            
        Returns:
            dict: A status dictionary containing:
                - status: 'success' or 'error'
                - message: A description of the result
                
        Thread-safe: Uses lock to ensure safe file operations.
        """
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
        """
        Retrieve tasks, optionally filtered by user.
        
        Parameters:
            user (str, optional): Username to filter tasks by. If provided,
                returns only tasks where user is creator or assignee.
                
        Returns:
            list: A list of task dictionaries matching the filter criteria.
                Returns empty list on error.
        """
        try:
            with open(self.tasks_file, 'r') as f:
                tasks = json.load(f)
            if user:
                return [t for t in tasks if t['assignee'] == user or t['creator'] == user]
            return tasks
        except Exception as e:
            return []

    def add_note(self, user, title, content, tags=None):
        """
        Add a new note to the system.
        
        Parameters:
            user (str): Username of the note creator
            title (str): Title of the note
            content (str): Content/body of the note
            tags (list, optional): List of tags to categorize the note
            
        Returns:
            dict: A status dictionary containing:
                - status: 'success' or 'error'
                - message: A description of the result
                
        Thread-safe: Uses lock to ensure safe file operations.
        """
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
        """
        Retrieve notes with optional filtering by user and/or tag.
        
        Parameters:
            user (str, optional): Username to filter notes by
            tag (str, optional): Tag to filter notes by
            
        Returns:
            list: A list of note dictionaries matching the filter criteria.
                Returns empty list on error.
                
        Notes:
            - If both user and tag are provided, returns notes matching both criteria
            - If neither is provided, returns all notes
        """
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
        """
        Search notes by their content, title, or tags.
        
        Parameters:
            query (str): The search query string
            
        Returns:
            list: A list of note dictionaries where the query matches:
                - Note content (case-insensitive)
                - Note title (case-insensitive)
                - Note tags (case-insensitive)
                Returns empty list on error.
        """
        try:
            with open(self.notes_file, 'r') as f:
                notes = json.load(f)
            return [n for n in notes if query.lower() in n['content'].lower() or 
                   query.lower() in n['title'].lower() or 
                   any(query.lower() in tag.lower() for tag in n['tags'])]
        except Exception as e:
            return []

    def share_note(self, note_id, shared_with):
        """
        Share an existing note with another user.
        
        Parameters:
            note_id (str): The unique identifier of the note to share
            shared_with (str): Username of the user to share the note with
            
        Returns:
            dict: A status dictionary containing:
                - status: 'success' or 'error'
                - message: A description of the result
                
        Thread-safe: Uses lock to ensure safe file operations.
        """
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
<environment_details>
# VSCode Visible Files
../../../../80
models/scan_target.py
requirements.txt
requirements.txt
services/__init__.py
services/__init__.py
ai_integration.py
ai_integration.py
main_window.py
main_window.py
../../../../79
models/__init__.py
../../.vscode/extensions/danielsanmedium.dscodegpt-3.8.61/standalone/accessible-view-terminal
../../.vscode/extensions/danielsanmedium.dscodegpt-3.8.61/standalone/extension-output-ms-vscode.cpptools-#2-cpptools
services/contribution_system.py

# VSCode Open Tabs
ai_module.py
ai_training.py
analytics_system.py
chat_system.py
codebreaker.py
collaboration_dialog.py
collaboration_system.py
contribution_system.py
database.py
login_dialog.py
main_gui.py
middleware.py
models.py
write_check.py
write_test.py
tabs/ai_chatbot_tab.py
tabs/amass_tab.py
tabs/bug_bounty_target_tab.py
Nuclei/add_nuclei_templates.py
Nuclei/template_schema.py
Nuclei/template_defaults.py
Nuclei/nuclei_template_model.py
Nuclei/test_doc.py
Nuclei/test_cython_templating.py
Nuclei/templates.py
src/integrated_app.py
update_tools.py
report_generator.py
Nuclei/nuclei_analyzer.py
ai_models.py
models/scan_target.py
tabs/nuclei_tab.py
models/__init__.py
services/vulnerability_scanner.py
main.py
tabs/__init__.py
services/__init__.py
tabs/ai_chat_tab.py
services/ai_system.py
ai_integration.py
.git/COMMIT_EDITMSG
scanning_profiles.py
setup_database.py
tabs/scope_tab.py
tabs/report_generator.py
tabs/shodan_tab.py
tabs/wayback_tab.py
main_window.py
tabs/scanner_tab.py
tabs/tool_manager_tab.py
tool_manager.py
services/contribution_system.py
setup_environment.py
shodan_integration.py
simple_log_test.py
test_openai_config.py
test_openai_console.py
test_openai_direct.py
test_openai_file.py
vulnerability_database.py
    def __init__(self, config=None):
        self.config = config or {}
        self.collaboration = Collaboration()
        self.collaboration_dialog = CollaborationDialog()
        self.contribution_dialog = ContributionDialog()
        self.contribution_system = ContributionSystem()
        self.notification = NotificationSystem()
        
    def initialize(self):
        """Initialize all collaboration subsystems"""
        # Setup notification system
        self.notification.initialize()
        
        # Initialize collaboration features
        self.collaboration.initialize()
        
        # Setup contribution system
        self.contribution_system.initialize()
        
    def share_report(self, report_data):
        """Share a report with collaborators"""
        # Process the report
        processed_report = self.collaboration.process_report(report_data)
        
        # Send notifications
        self.notification.notify_collaborators(processed_report)
        
        # Log contribution
        self.contribution_system.log_contribution(processed_report)
        
        return processed_report
        
    def get_collaboration_status(self):
        """Get status of all collaboration subsystems"""
        return {
            'collaboration_status': self.collaboration.get_status(),
            'contribution_status': self.contribution_system.get_status(),
            'notification_status': self.notification.get_status()
        }
        
    def show_collaboration_dialog(self):
        """Show the collaboration dialog"""
        return self.collaboration_dialog.show()
        
    def show_contribution_dialog(self):
        """Show the contribution dialog"""
        return self.contribution_dialog.show()
