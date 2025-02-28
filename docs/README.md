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

- **AI-Powered Analysis**: Integrated AI models for vulnerability detection and analysis.
- **Vulnerability Scanning**: Comprehensive scanning using Nuclei and custom tools.
- **Tool Management**: Manage and integrate external security tools.
- **Collaboration Features**: Share scan results and collaborate with team members.
- **Security System Integration**: Integrate with external security systems.
- **External Tool Integration**: Seamless integration with tools like Amass and Nuclei.

## Project Structure

- `main.py` - Main application entry point
- `src/` - Core source files
  - `scanning/` - Scanning functionalities
  - `ai/` - AI models and analysis
  - `gui/` - GUI components
  - `models/` - Data models
  - `settings/` - Configuration management
- `services/` - Core services and business logic
  - `vulnerability_scanner.py` - Vulnerability scanning service
  - `scan_service.py` - Scan management service
- `tabs/` - UI components and tab implementations
  - `scanner_tab.py` - Scanner interface
  - `vulnerability_tab.py` - Vulnerability analysis interface
  - `nuclei_tab.py` - Nuclei scanning interface
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
