import os
def safe_read_file(filepath, fallback_path=None):
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        if fallback_path:
            print(f"[INFO] Trying fallback path: {fallback_path}")
            return safe_read_file(fallback_path)
        return None
    except PermissionError:
        print(f"[ERROR] Permission denied for file: {filepath}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error reading file {filepath}: {str(e)}")
        return None
data = safe_read_file("examples/from_mouther/input.csv", fallback_path="examples/from_mouther/default.csv")
if data:
    print("File read successfully!")
else:
    print("Could not read the file.")