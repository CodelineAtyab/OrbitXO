import pandas as pd
import os

class SimpleCSVReader:
    """
    A simple CSV reader that handles common errors gracefully
    """
    
    def read_csv_safe(self, file_path, backup_file=None):
 
        # Try to read the main file first
        result = self._try_read_file(file_path)
        if result is not None:
            print(f"✅ Successfully read: {file_path}")
            return result
        
        # If main file failed and backup exists, try backup
        if backup_file:
            print(f"⚠️  Main file failed, trying backup: {backup_file}")
            result = self._try_read_file(backup_file)
            if result is not None:
                print(f"✅ Successfully read backup: {backup_file}")
                return result
        
        # All attempts failed
        print("❌ All file reading attempts failed")
        return None
    
    def _try_read_file(self, file_path):
        """
        Try to read a single CSV file with common error handling
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            pandas DataFrame or None if failed
        """
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        # Check if we can read the file
        if not os.access(file_path, os.R_OK):
            print(f"❌ Permission denied: {file_path}")
            return None
        
        # Check if file is empty
        if os.path.getsize(file_path) == 0:
            print(f"⚠️  File is empty: {file_path}")
            return pd.DataFrame()  # Return empty DataFrame
        
        # Try different ways to read the CSV
        # Method 1: Default pandas settings
        try:
            data = pd.read_csv(file_path)
            print("✅ Read successful using method 1 (default)")
            print(f"📊 Data shape: {data.shape[0]} rows, {data.shape[1]} columns")
            return data
        except Exception as e:
            print(f"⚠️  Method 1 failed: {str(e)[:50]}...")
        
        # Method 2: Handle encoding issues
        try:
            data = pd.read_csv(file_path, encoding='latin-1')
            print("✅ Read successful using method 2 (latin-1 encoding)")
            print(f"📊 Data shape: {data.shape[0]} rows, {data.shape[1]} columns")
            return data
        except Exception as e:
            print(f"⚠️  Method 2 failed: {str(e)[:50]}...")
        
        # Method 3: Different separator (semicolon)
        try:
            data = pd.read_csv(file_path, sep=';')
            print("✅ Read successful using method 3 (semicolon separator)")
            print(f"📊 Data shape: {data.shape[0]} rows, {data.shape[1]} columns")
            return data
        except Exception as e:
            print(f"⚠️  Method 3 failed: {str(e)[:50]}...")
        
        # Method 4: Skip bad lines
        try:
            data = pd.read_csv(file_path, on_bad_lines='skip')
            print("✅ Read successful using method 4 (skip bad lines)")
            print(f"📊 Data shape: {data.shape[0]} rows, {data.shape[1]} columns")
            return data
        except Exception as e:
            print(f"⚠️  Method 4 failed: {str(e)[:50]}...")
        
        # Method 5: No header assumption
        try:
            data = pd.read_csv(file_path, header=None)
            print("✅ Read successful using method 5 (no header)")
            print(f"📊 Data shape: {data.shape[0]} rows, {data.shape[1]} columns")
            return data
        except Exception as e:
            print(f"⚠️  Method 5 failed: {str(e)[:50]}...")

        
        # All methods failed
        print(f"❌ Could not read file with any method: {file_path}")
        return None
    
    def get_file_info(self, file_path):
        """
        Get basic information about the file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file info
        """
        info = {
            'file_exists': os.path.exists(file_path),
            'can_read': False,
            'file_size': 0,
            'is_empty': True
        }
        
        if info['file_exists']:
            info['can_read'] = os.access(file_path, os.R_OK)
            info['file_size'] = os.path.getsize(file_path)
            info['is_empty'] = info['file_size'] == 0
        
        return info


# Example usage
def example_usage():
    """
    Show how to use the SimpleCSVReader
    """
    
    # Create reader
    reader = SimpleCSVReader()
    
    # Example 1: Read a CSV file with backup
    print("=== Example 1: Reading CSV with backup ===")
    data = reader.read_csv_safe(
        file_path='sales_data.csv',
        backup_file='sales_backup.csv'
    )
    
    if data is not None and not data.empty:
        print("Data preview:")
        print(data.head())
        print(f"Total rows: {len(data)}")
    else:
        print("No data was loaded")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Check file info before reading
    print("=== Example 2: Check file info first ===")
    file_info = reader.get_file_info('sales_data.csv')
    print(f"File info: {file_info}")
    
    if file_info['file_exists'] and file_info['can_read'] and not file_info['is_empty']:
        print("File looks good, attempting to read...")
        data = reader.read_csv_safe('sales_data.csv')
        if data is not None:
            print(f"Successfully loaded {len(data)} rows")
    else:
        print("File has issues, skipping read attempt")


# To run the example, uncomment the line below:
# example_usage()