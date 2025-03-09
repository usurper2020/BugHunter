# Basic usage
python fix_all_issues.py

# Fix a single file
python -m code_fixer my_script.py

# Fix specific issues
python -m code_fixer my_script.py --fixers style imports

# Fix a directory recursively
python -m code_fixer my_project/ --recursive

# Non-interactive mode with no backups
python -m code_fixer my_script.py --non-interactive --no-backup

# Exclude specific folders
python fix_all_issues.py --exclude tests docs backups

# Use verbose logging
python fix_all_issues.py --verbose

#Dry run with verbose output
python fix_all_issues.py --dry-run --verbose

# Specify root directory and exclude folders:
python fix_all_issues.py --root ./my_project --exclude tests docs temp

# Run specific fixers only:
python fix_all_issues.py --fixers imports style

# Specify root directory and excludes
python fix_all_issues.py --root ./my_project --exclude tests backups

# Exclude specific folders
python fix_all_issues.py --exclude tests docs backups

# Use verbose logging
python fix_all_issues.py --verbose

# Specify root directory and excludes
python fix_all_issues.py --root ./my_project --exclude tests backups

# Custom backup directory and log file:
python fix_all_issues.py --backup-dir ./backups --log-file ./logs/fix.log

# Process specific file types with size limit:
python fix_all_issues.py --file-pattern "*.pyw" --max-size 2097152