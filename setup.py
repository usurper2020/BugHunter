from setuptools import setup, find_packages

setup(
    name="bughunter",
    version="0.1",
    packages=find_packages(include=['src', 'src.*']),

    install_requires=[
        'PyQt6',
        'sqlalchemy',
        'psycopg2',
        'bcrypt',
        'python-dateutil',
        'graphviz'

    ],
    entry_points={
        'console_scripts': [
            'bughunter=src.main:main',
        ],
    },
)
