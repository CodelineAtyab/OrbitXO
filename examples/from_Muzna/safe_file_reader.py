import sys
def safe_read_file(filename):#examples/from_Muzna/data.txt
    try:
        with open(filename, "r") as file:
            content = file.read()
            print(f"Successfully read: {filename}")
    except FileNotFoundError:
        print("File not found. Please check the filename.")
        with open("filename", "w") as f:
            f.write("")  # Create it
        content = ""
    except PermissionError:
        print("Permission denied. Try running with elevated privileges.")
    except UnicodeDecodeError:
        print("Corrupt or invalid file format. Cannot read as text.")
    except Exception as e:
        print("Unexpected error:", e)
    return content


if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Usage: python safe_reader.py <filename>")
    else:
        filename = sys.argv[1]
        content = safe_read_file(filename)
        print("\n--- File Content Start ---\n")
        print(content)
        print("\n--- File Content End ---")