#!/usr/bin/env python
"""
Quick Start script for Shark Tank with PostgreSQL
Automates the entire setup process
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_postgresql():
    """Check if PostgreSQL is accessible"""
    print("🔍 Checking PostgreSQL connection...")
    
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USERNAME', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password')
        )
        conn.close()
        print("✅ PostgreSQL is accessible!")
        return True
    except ImportError:
        print("❌ psycopg2 not installed. Installing dependencies first...")
        return False
    except Exception as e:
        print(f"❌ Cannot connect to PostgreSQL: {e}")
        print("Please ensure PostgreSQL is running and accessible.")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    if run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("✅ Dependencies installed successfully!")
        return True
    else:
        print("❌ Failed to install dependencies")
        return False

def setup_database():
    """Set up the database"""
    print("🗄️ Setting up database...")
    
    if run_command("python setup_database.py", "Database setup"):
        print("✅ Database setup completed!")
        return True
    else:
        print("❌ Database setup failed")
        return False

def test_functionality():
    """Test the database functionality"""
    print("🧪 Testing database functionality...")
    
    if run_command("python test_database.py", "Database functionality test"):
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

def main():
    """Main setup function"""
    print("🚀 Shark Tank PostgreSQL Quick Start")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("❌ Please run this script from the shark_tank directory")
        print("   cd shark_tank")
        print("   python quick_start.py")
        return False
    
    print("\nThis script will:")
    print("1. Install Python dependencies")
    print("2. Set up PostgreSQL database")
    print("3. Test the functionality")
    print("4. Provide instructions for running the app")
    
    response = input("\nContinue? (y/N): ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        return False
    
    # Step 1: Install dependencies
    if not install_dependencies():
        return False
    
    # Step 2: Check PostgreSQL
    if not check_postgresql():
        print("\nPlease ensure PostgreSQL is running and try again.")
        return False
    
    # Step 3: Setup database
    if not setup_database():
        return False
    
    # Step 4: Test functionality
    if not test_functionality():
        return False
    
    # Success!
    print("\n" + "="*50)
    print("🎉 Setup completed successfully!")
    print("\nYou can now run the Shark Tank application:")
    print("\nOption 1: Run from current directory")
    print("  python -m shark_tank.main")
    print("\nOption 2: Run from src directory")
    print("  cd src")
    print("  python -m shark_tank.main")
    print("\nOption 3: Run the main script directly")
    print("  cd src/shark_tank")
    print("  python main.py")
    
    print("\nThe application will now store all pitch and Q&A data in PostgreSQL,")
    print("ensuring sharks can make decisions based on complete conversation history!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
