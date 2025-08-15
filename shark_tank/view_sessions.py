#!/usr/bin/env python
"""
Simple Session Viewer for Shark Tank
Shows active sessions and their IDs for easy reference
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from shark_tank.session_manager import SessionManager

def view_sessions():
    """View all active sessions"""
    print("🦈 Shark Tank Session Viewer")
    print("=" * 50)
    
    try:
        session_mgr = SessionManager()
        sessions = session_mgr.list_active_sessions()
        
        if not sessions:
            print("📊 No active sessions found.")
            print("\nTo create a session, run the main application:")
            print("  python -m shark_tank.main")
            return
        
        print(f"📊 Found {len(sessions)} active session(s):")
        print()
        
        for session in sessions:
            print(f"  Session #{session['session_number']}")
            print(f"    ID: {session['session_id']}")
            print(f"    Pitch: {session['pitch_text']}")
            print(f"    Created: {session['created_at']}")
            print()
        
        print("💡 To continue with a session:")
        print("  1. Run: python -m shark_tank.main")
        print("  2. Choose option 2 (Continue with existing session)")
        print("  3. Enter the session ID from above")
        print()
        print("💡 To refresh a session:")
        print("  1. Run: python -m shark_tank.main")
        print("  2. Choose option 3 (Refresh existing session)")
        print("  3. Enter the session ID from above")
        
    except Exception as e:
        print(f"❌ Error viewing sessions: {e}")

def main():
    """Main function"""
    view_sessions()

if __name__ == "__main__":
    main()
