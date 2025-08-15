#!/usr/bin/env python
"""
Database setup script for Shark Tank application
This script helps set up PostgreSQL database and tables
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Create the shark_tank database if it doesn't exist"""
    
    # Database connection parameters
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    username = os.getenv('DB_USERNAME', 'postgres')
    password = os.getenv('DB_PASSWORD', 'postgres')
    database_name = os.getenv('DB_NAME', 'shark_tank')
    
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database_name,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{database_name}'...")
            cursor.execute(f'CREATE DATABASE "{database_name}"')
            print(f"✅ Database '{database_name}' created successfully!")
        else:
            print(f"✅ Database '{database_name}' already exists!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is installed and running")
        print("2. The connection parameters are correct")
        print("3. The user has permission to create databases")
        return False

def test_connection():
    """Test connection to the shark_tank database"""
    
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    username = os.getenv('DB_USERNAME', 'postgres')
    password = os.getenv('DB_PASSWORD', 'postgres')
    database_name = os.getenv('DB_NAME', 'shark_tank')
    
    try:
        # Connect to the specific database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database_name
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Successfully connected to database '{database_name}'")
        print(f"PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error connecting to database '{database_name}': {e}")
        return False

def create_tables():
    """Create the necessary tables in the database"""
    
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    username = os.getenv('DB_USERNAME', 'postgres')
    password = os.getenv('DB_PASSWORD', 'postgres')
    database_name = os.getenv('DB_NAME', 'shark_tank')
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database_name
        )
        
        cursor = conn.cursor()
        
        # Create pitch_sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pitch_sessions (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(100) UNIQUE NOT NULL,
                pitch_text TEXT NOT NULL,
                amount_invested INTEGER NOT NULL,
                percentage_equity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create qa_entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qa_entries (
                id SERIAL PRIMARY KEY,
                pitch_session_id INTEGER REFERENCES pitch_sessions(id) ON DELETE CASCADE,
                shark_name VARCHAR(100) NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                round_number INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pitch_sessions_session_id ON pitch_sessions(session_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_qa_entries_pitch_session_id ON qa_entries(pitch_session_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_qa_entries_shark_name ON qa_entries(shark_name);")
        
        conn.commit()
        print("✅ Tables created successfully!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Shark Tank PostgreSQL Database...\n")
    
    # Step 1: Create database
    if not create_database():
        sys.exit(1)
    
    # Step 2: Test connection
    if not test_connection():
        sys.exit(1)
    
    # Step 3: Create tables
    if not create_tables():
        sys.exit(1)
    
    print("\n🎉 Database setup completed successfully!")
    print("\nYou can now run the Shark Tank application.")
    print("\nTo customize database settings, set these environment variables:")
    print("  DB_HOST - PostgreSQL host (default: localhost)")
    print("  DB_PORT - PostgreSQL port (default: 5432)")
    print("  DB_NAME - Database name (default: shark_tank)")
    print("  DB_USERNAME - Username (default: postgres)")
    print("  DB_PASSWORD - Password (default: password)")

if __name__ == "__main__":
    main()
