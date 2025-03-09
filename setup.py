from setuptools import setup, find_packages
from os import path

# Read the contents of README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read the requirements
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="bughunter",
    version="1.0.0",
    author="Bug Hunter Project Contributors",
    author_email="your.email@example.com",
    description="A comprehensive tool for bug bounty hunters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bughunter",
    packages=find_packages(exclude=['tests*', 'docs*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=required,
    entry_points={
        'console_scripts': [
            'bughunter=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'bughunter': [
            'data/*.json',
            'docs/*.md',
            'tools/*',
        ],
    },
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.3.0',
            'flake8>=4.0.1',
            'mypy>=0.910',
            'bandit>=1.7.0',
        ],
        'docs': [
            'mkdocs>=1.2.3',
            'mkdocs-material>=8.1.3',
            'mkdocstrings>=0.16.2',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/bughunter/issues',
        'Source': 'https://github.com/yourusername/bughunter',
        'Documentation': 'https://github.com/yourusername/bughunter/docs',
    },
    keywords=[
        'security',
        'bug-bounty',
        'vulnerability-scanner',
        'penetration-testing',
        'security-tools',
        'hacking',
        'cybersecurity',
    ],
)
