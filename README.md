# Bug Hunter

A comprehensive security tool featuring AI chat, vulnerability scanning, and tool management capabilities.

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/BugHunter.git
cd BugHunter
```

2. Create a virtual environment (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Make sure you have a `config.json` file with your API keys:

```json
{
    "AI_API_KEY": "your-openai-api-key",
    "JWT_SECRET_KEY": "your-jwt-secret-key",
    "JWT_EXPIRATION_HOURS": 24,
    "TOOLS_DIRECTORY": "tools",
    "REPORTS_DIRECTORY": "reports",
    "CACHE_DIRECTORY": "cache",
    "MAX_CONCURRENT_SCANS": 5,
    "SCAN_TIMEOUT_MINUTES": 30,
    "DEFAULT_SCAN_DEPTH": "medium",
    "ENABLE_COLLABORATION": true,
    "ENABLE_ANALYTICS": true
}
```

## Running the Application

1. Start the application:

```bash
python main.py
```

2. Login or Register:
   - Default admin credentials:
     - Username: admin
     - Password: admin
   - Or register a new account with:
     - Username: 3+ characters (letters, numbers, underscores, hyphens)
     - Password requirements:
       - Minimum 8 characters
       - At least one uppercase letter
       - At least one lowercase letter
       - At least one number
       - At least one special character (!@#$%^&*(),.?":{}|<>)

## Features

- **User Authentication**
  - Secure login system
  - User registration with password validation
  - JWT token-based authentication
  - Role-based access control

- **AI Chat Assistant**
  - Dark-themed chat interface
  - OpenAI API integration
  - Real-time responses

- **Vulnerability Scanner**
  - Multiple scan types (Quick, Full, Custom)
  - Progress tracking
  - Detailed reporting

- **Tool Management**
  - GitHub integration
  - Automatic tool installation
  - Multi-language support

## Directory Structure

```
BugHunter/
├── main.py           # Main entry point
├── config.json       # Configuration file
├── requirements.txt  # Dependencies
├── services/         # Core services
│   ├── user_auth.py
│   ├── tool_manager.py
│   └── vulnerability_scanner.py
├── tabs/            # UI components
│   ├── ai_chat_tab.py
│   └── tool_tab.py
├── logs/            # Log files
├── tools/           # Downloaded tools
├── reports/         # Scan reports
└── cache/           # Cache directory
```

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

2. Check if the required directories exist:

```bash
python -c "import os; [os.makedirs(d, exist_ok=True) for d in ['logs', 'tools', 'reports', 'cache']]"
```

3. Verify your config.json file has all required keys and valid values.

4. Make sure you're using Python 3.7 or higher:

```bash
python --version
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
