import os
import shutil

# Path to the invalid distribution
invalid_dist_path = (
    r"C:\Users\clabb\AppData\Local\Programs\Python\Python311\Lib\site-packages\~ytest"
)

# Remove the directory if it exists
if os.path.exists(invalid_dist_path):
    try:
        shutil.rmtree(invalid_dist_path)
        print("Successfully removed invalid distribution")
    except Exception as e:
        print(f"Error removing directory: {e}")
