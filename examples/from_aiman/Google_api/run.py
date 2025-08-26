import os
import sys
import subprocess

def main():
    """
    Simple wrapper to run the main application with the correct Python environment
    and ensure proper imports.
    """
    print("Travel Time Tracker Runner")
    print("==========================")
    
   
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    
    os.chdir(script_dir)
    
    if os.name == 'nt':  
        python_executable = os.path.join(script_dir, '.venv', 'Scripts', 'python.exe')
    else:  
        python_executable = os.path.join(script_dir, '.venv', 'bin', 'python')
    

    if not os.path.exists(python_executable):
        print(f"Error: Python executable not found at {python_executable}")
        print("Please make sure the virtual environment is set up correctly.")
        return 1
    
    
    main_app = os.path.join(script_dir, 'main_app.py')
    
    
    print(f"Running main application with {python_executable}")
    try:
        result = subprocess.run([python_executable, main_app], check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running main application: {e}")
        return e.returncode
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
