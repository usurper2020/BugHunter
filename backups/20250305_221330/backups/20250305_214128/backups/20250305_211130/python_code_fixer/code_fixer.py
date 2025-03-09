from code_fixer import CodeFixer


directory = ""
# As a module

fixer = CodeFixer()

# Fix a single file
results = fixer.fix_file("my_script.py")

# Fix specific issues in a file
results = fixer.fix_file("my_script.py", fixers=["style", "imports"])

# Fix an entire directory
results = fixer.fix_directory("my_project/")

# Print report
fixer.print_report()
