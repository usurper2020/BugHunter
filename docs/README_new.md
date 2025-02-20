# Bug Hunter

A comprehensive tool for bug bounty hunters, featuring vulnerability scanning, collaboration, and AI-powered analysis capabilities.

## Features

- **AI-Powered Analysis**: Integrated CodeGPT chat widget for real-time assistance
- **Vulnerability Scanning**: Advanced scanning capabilities
- **Collaboration**: Team collaboration features
- **Analytics**: Detailed analysis and reporting
- **Security**: Strong authentication and encryption

## AI Integration

The application includes an integrated CodeGPT chat widget that provides:

- Real-time AI assistance for bug hunting
- Vulnerability analysis help
- Security recommendations
- Code review assistance
- Best practices guidance

### Setting up CodeGPT

1. Get your CodeGPT API key:
   - Visit <https://codegpt.co>
   - Sign up/Login to your account
   - Generate an API key
   - The widget ID is already configured: `83b8e7bc-6f29-4501-8690-2b1220a9c581`

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bughunter.git
cd bughunter
```

2. Run the installation script:

```bash
# With CodeGPT API key
python install.py --api-key YOUR_CODEGPT_API_KEY

# Without API key (configure later)
python install.py
```

3. Activate the virtual environment:

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Run the application:

```bash
python run.py
```

## Configuration

The installation script creates a `config.json` file with secure defaults. You can modify these settings:

- `AI_API_KEY`: Your CodeGPT API key
- `DB_PASSWORD`: Database password
- Other settings as needed

## Features

### AI Assistant

- Real-time chat with CodeGPT
- Security analysis
- Code review
- Best practices recommendations

### Vulnerability Scanner

- Security header checks
- SSL/TLS analysis
- Common vulnerability detection
- Detailed reporting

### Security

- Strong authentication
- Rate limiting
- Input validation
- Secure session management

## Development

Requirements:

- Python 3.8+
- PostgreSQL database
- Redis (optional, for caching)

Development setup:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python run_tests.py
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support:

- Open an issue
- Check documentation
- Contact development team

## Acknowledgments

- CodeGPT for AI capabilities
- OWASP for security guidelines
- Open source community
