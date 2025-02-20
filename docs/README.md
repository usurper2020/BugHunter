# Bug Hunter

A comprehensive security tool featuring AI chat, vulnerability scanning, and tool management capabilities.

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

The application has a single entry point through `main.py`:

```bash
python main.py
```

## Features

- AI-Powered Analysis
- Vulnerability Scanning
- Tool Management
- Collaboration Features
- Security System Integration
- External Tool Integration (Amass, Nuclei)

## Project Structure

- `main.py` - Main application entry point
- `services/` - Core services and business logic
- `tabs/` - UI components and tab implementations
- `config/` - Configuration files
- `data/` - Data storage
- `logs/` - Application logs
- `tools/` - External tool integrations
- `reports/` - Generated reports

## Configuration

The application uses a centralized configuration system. Main configuration files:

- `config/system_config.json` - System-wide configuration
- `config.json` - Local configuration overrides

## Development

The project follows a modular architecture:

1. Core services in `services/`
2. UI components in `tabs/`
3. Single entry point through `main.py`
4. Configuration management through `services/config_manager.py`

## License

See LICENSE file for details.
