"""
MySQL Database Configuration

This module contains configuration information for the MySQL database connection.
"""
import os
import sys
from dotenv import load_dotenv, find_dotenv

# Find and load the .env file from the current directory
dotenv_path = find_dotenv()
if dotenv_path:
    print(f"Found .env file at: {dotenv_path}")
    load_dotenv(dotenv_path)
else:
    print("Warning: .env file not found!")
    # Try direct path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_dir, '.env')
    if os.path.exists(env_path):
        print(f"Loading .env file from direct path: {env_path}")
        load_dotenv(env_path)
    else:
        print(f"No .env file found at: {env_path}")

# MySQL Configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', '3306')),
    'user': os.getenv('MYSQL_USER', 'route_user'),
    'password': os.getenv('MYSQL_PASSWORD', 'route_password'),
    'database': os.getenv('MYSQL_DATABASE', 'route_tracker'),
}

# Docker Configuration
DOCKER_MYSQL_IMAGE = 'mysql:8.0'
DOCKER_MYSQL_CONTAINER = 'google_maps_mysql'
DOCKER_BUILD_PATH = os.path.dirname(os.path.abspath(__file__))

# Export these functions
def get_db_config():
    """Return the database configuration parameters"""
    return MYSQL_CONFIG

def check_docker_running():
    """Check if Docker is running on the system"""
    try:
        import docker
        client = docker.from_env()
        client.ping()
        return client
    except ImportError:
        print("Docker SDK for Python is not installed. Run 'pip install docker' to install it.")
        return None
    except Exception as e:
        print(f"Docker is not running or not accessible: {e}")
        return None

# Print configuration details for debugging
print(f"DB_CONFIG module loaded with host: {MYSQL_CONFIG['host']}, database: {MYSQL_CONFIG['database']}")
