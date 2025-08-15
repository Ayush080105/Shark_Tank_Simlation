#!/usr/bin/env python
"""
Configuration utility for Shark Tank application
Helps users set up database environment variables
"""

import os
import sys

def create_env_file():
    """Create a .env file with database configuration"""
    
    env_content = """# Database Configuration for Shark Tank
# Update these values according to your PostgreSQL setup

DB_HOST=localhost
DB_PORT=5432
DB_NAME=shark_tank
DB_USERNAME=postgres
DB_PASSWORD=your_password

# Optional: Custom connection string (overrides individual settings above)
# DB_CONNECTION_STRING=postgresql://username:password@host:port/database
"""
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_file_path):
        print(f"⚠️  .env file already exists at {env_file_path}")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Configuration cancelled.")
            return False
    
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print(f"✅ .env file created at {env_file_path}")
        print("Please update the values according to your PostgreSQL setup.")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def show_current_config():
    """Show current database configuration"""
    
    print("Current Database Configuration:")
    print("=" * 40)
    
    config_vars = [
        'DB_HOST', 'DB_PORT', 'DB_NAME', 
        'DB_USERNAME', 'DB_PASSWORD', 'DB_CONNECTION_STRING'
    ]
    
    for var in config_vars:
        value = os.getenv(var, 'Not set')
        if var == 'DB_PASSWORD' and value != 'Not set':
            value = '*' * len(value)  # Mask password
        print(f"{var}: {value}")
    
    print("\nDefault values will be used for unset variables:")
    print("  DB_HOST: localhost")
    print("  DB_PORT: 5432")
    print("  DB_NAME: shark_tank")
    print("  DB_USERNAME: postgres")
    print("  DB_PASSWORD: password")

def main():
    """Main configuration function"""
    
    print("🔧 Shark Tank Database Configuration Utility\n")
    
    while True:
        print("\nOptions:")
        print("1. Show current configuration")
        print("2. Create .env file template")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == '1':
            show_current_config()
        elif choice == '2':
            create_env_file()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
