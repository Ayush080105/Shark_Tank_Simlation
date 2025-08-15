#!/usr/bin/env python
"""
Session Management Utility for Shark Tank
Allows users to manage their sessions independently
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from shark_tank.session_manager import SessionManager
from shark_tank.database import DatabaseManager

class SessionManagerCLI:
    """Command-line interface for session management"""
    
    def __init__(self):
        """Initialize the session manager CLI"""
        self.session_manager = SessionManager()
        self.db_manager = DatabaseManager()
    
    def show_menu(self):
        """Show the main menu"""
        print("\n" + "="*60)
        print("🦈 Shark Tank Session Manager")
        print("="*60)
        print("1. View all sessions")
        print("2. View session details")
        print("3. Refresh a session (keep pitch, reset Q&A)")
        print("4. Reset to session 1")
        print("5. View session statistics")
        print("6. Test database connection")
        print("7. Exit")
        print("="*60)
    
    def view_all_sessions(self):
        """View all active sessions"""
        print("\n📊 Active Sessions:")
        sessions = self.session_manager.list_active_sessions()
        
        if not sessions:
            print("  No active sessions found.")
            return
        
        for session in sessions:
            print(f"\n  Session #{session['session_number']}")
            print(f"    ID: {session['session_id']}")
            print(f"    Pitch: {session['pitch_text']}")
            print(f"    Created: {session['created_at']}")
    
    def view_session_details(self):
        """View details of a specific session"""
        session_id = input("\nEnter session ID (or press Enter to skip): ").strip()
        if not session_id:
            return
        
        session = self.session_manager.get_session(session_id)
        if not session:
            print(f"❌ Session {session_id} not found.")
            return
        
        print(f"\n📋 Session #{session['session_number']} Details:")
        print(f"  ID: {session['session_id']}")
        print(f"  Created: {session['created_at']}")
        print(f"  Current Round: {session['current_round']}")
        print(f"  Total Q&A Rounds: {len(session['qa_rounds'])}")
        
        if session['pitch_data']:
            print(f"\n  Pitch Data:")
            for key, value in session['pitch_data'].items():
                print(f"    {key}: {value}")
        
        if session['qa_rounds']:
            print(f"\n  Q&A History:")
            for i, qa in enumerate(session['qa_rounds'], 1):
                print(f"    Round {i}: {qa['shark_name']}")
                print(f"      Q: {qa['question']}")
                print(f"      A: {qa['answer']}")
                print(f"      Time: {qa['timestamp']}")
    
    def refresh_session(self):
        """Refresh a session (keep pitch, reset Q&A)"""
        session_id = input("\nEnter session ID to refresh: ").strip()
        if not session_id:
            return
        
        try:
            new_session_id = self.session_manager.refresh_session(session_id)
            print(f"✅ Session refreshed successfully!")
            print(f"  Old Session ID: {session_id}")
            print(f"  New Session ID: {new_session_id}")
            print(f"  New Session Number: #{self.session_manager.get_session(new_session_id)['session_number']}")
            print("  Pitch data preserved, Q&A reset to round 1")
        except ValueError as e:
            print(f"❌ Error refreshing session: {e}")
    
    def reset_to_session_1(self):
        """Reset completely to session 1"""
        confirm = input("\n⚠️  This will clear ALL active sessions. Are you sure? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Reset cancelled.")
            return
        
        try:
            new_session_id = self.session_manager.reset_to_session_1()
            print(f"✅ Reset to session 1 successful!")
            print(f"  New Session ID: {new_session_id}")
            print(f"  All previous sessions cleared")
            print(f"  Starting fresh with session #1")
        except Exception as e:
            print(f"❌ Error resetting sessions: {e}")
    
    def view_statistics(self):
        """View session statistics"""
        stats = self.session_manager.get_session_stats()
        
        print(f"\n📈 Session Statistics:")
        print(f"  Total Active Sessions: {stats['total_active_sessions']}")
        print(f"  Total Q&A Rounds: {stats['total_qa_rounds']}")
        print(f"  Next Session Number: {stats['next_session_number']}")
        
        if stats['sessions']:
            print(f"\n  Active Sessions:")
            for session in stats['sessions']:
                print(f"    #{session['session_number']}: {session['pitch_text']}")
    
    def test_database(self):
        """Test database connection"""
        print("\n🔍 Testing Database Connection...")
        
        try:
            # Test basic connection
            test_session = self.db_manager.get_session()
            test_session.close()
            print("✅ Database connection successful!")
            
            # Test table creation
            print("✅ Database tables accessible!")
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("  Please ensure PostgreSQL is running and accessible.")
    
    def run(self):
        """Run the session manager CLI"""
        while True:
            self.show_menu()
            
            try:
                choice = input("\nSelect an option (1-7): ").strip()
                
                if choice == '1':
                    self.view_all_sessions()
                elif choice == '2':
                    self.view_session_details()
                elif choice == '3':
                    self.refresh_session()
                elif choice == '4':
                    self.reset_to_session_1()
                elif choice == '5':
                    self.view_statistics()
                elif choice == '6':
                    self.test_database()
                elif choice == '7':
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid option. Please select 1-7.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")
        
        # Cleanup
        self.db_manager.close()

def main():
    """Main function"""
    print("🚀 Starting Shark Tank Session Manager...")
    
    try:
        cli = SessionManagerCLI()
        cli.run()
    except Exception as e:
        print(f"❌ Failed to start session manager: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
