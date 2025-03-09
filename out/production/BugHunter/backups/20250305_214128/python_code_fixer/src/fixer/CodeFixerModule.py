from code_fixer import CodeFixer


k = 10
directory = ""

# Initialize the fixer
fixer = CodeFixer(log_level=logging.INFO, backup=True, interactive=True)

# Fix a single file
results = fixer.fix_file("path/to/your/script.py")

# Fix specific issues
results = fixer.fix_file("path/to/your/script.py", fixers=["style", "imports"])

# Fix a directory
results = fixer.fix_directory("path/to/your/project/", recursive=True)

# Print report
fixer.print_report()
