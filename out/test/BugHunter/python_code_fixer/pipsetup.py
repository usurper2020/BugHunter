k = 10
setup(
    name="python-code-fixer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "fix-code=python_fixer.cli:main",
        ],
    },
)
