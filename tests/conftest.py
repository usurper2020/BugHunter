import os
import sys
import pytest
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# Test data directory
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

@pytest.fixture
def test_data_dir():
    """Fixture to provide test data directory"""
    if not os.path.exists(TEST_DATA_DIR):
        os.makedirs(TEST_DATA_DIR)
    return TEST_DATA_DIR

@pytest.fixture
def mock_user_data():
    """Fixture to provide mock user data"""
    return {
        'username': 'testuser',
        'role': 'user',
        'created_at': '2024-01-01T00:00:00',
    }

@pytest.fixture
def mock_admin_data():
    """Fixture to provide mock admin data"""
    return {
        'username': 'admin',
        'role': 'admin',
        'created_at': '2024-01-01T00:00:00',
    }

@pytest.fixture
def mock_scan_result():
    """Fixture to provide mock scan result data"""
    return {
        'status': 'success',
        'results': {
            'id': 'scan_20240101_000000',
            'target': 'http://example.com',
            'timestamp': '2024-01-01T00:00:00',
            'findings': [
                {
                    'type': 'sql_injection',
                    'severity': 'critical',
                    'description': 'SQL Injection vulnerability',
                    'details': 'Parameter vulnerable to SQL injection'
                }
            ]
        }
    }

@pytest.fixture
def mock_report_data():
    """Fixture to provide mock report data"""
    return {
        'report_id': 'report_20240101_000000',
        'scan_id': 'scan_20240101_000000',
        'generated_at': '2024-01-01T00:00:00',
        'format': 'pdf',
        'content': 'Mock report content'
    }

@pytest.fixture
def clean_test_env(test_data_dir):
    """Fixture to set up and clean test environment"""
    # Create necessary test directories
    os.makedirs(os.path.join(test_data_dir, 'reports'), exist_ok=True)
    os.makedirs(os.path.join(test_data_dir, 'tools'), exist_ok=True)
    
    # Clean up any existing test files
    for root, dirs, files in os.walk(test_data_dir):
        for file in files:
            os.remove(os.path.join(root, file))
    
    yield test_data_dir
    
    # Cleanup after tests
    for root, dirs, files in os.walk(test_data_dir):
        for file in files:
            os.remove(os.path.join(root, file))

@pytest.fixture
def mock_preferences():
    """Fixture to provide mock preferences data"""
    return {
        'last_target': 'http://example.com',
        'shodan_api_key': 'mock_api_key',
        'theme': 'dark',
        'auto_save': True
    }

@pytest.fixture
def mock_collaboration_data():
    """Fixture to provide mock collaboration data"""
    return {
        'message': {
            'sender': 'testuser',
            'recipient': 'admin',
            'content': 'Test message',
            'timestamp': '2024-01-01T00:00:00'
        },
        'task': {
            'id': 'task_001',
            'title': 'Test task',
            'description': 'Test task description',
            'assignee': 'testuser',
            'status': 'pending'
        },
        'note': {
            'id': 'note_001',
            'title': 'Test note',
            'content': 'Test note content',
            'tags': ['test', 'documentation']
        }
    }

def pytest_configure(config):
    """Configure test environment"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Skip slow tests unless explicitly requested
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )
