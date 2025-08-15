#!/usr/bin/env python
"""
Test script for Shark Tank database functionality
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from shark_tank.database import DatabaseManager
from shark_tank.session_manager import SessionManager

def test_database_connection():
    """Test database connection and basic operations"""
    print("🧪 Testing Database Connection...")
    
    try:
        db = DatabaseManager()
        print("✅ Database connection successful!")
        
        # Test creating a pitch session
        pitch_session = db.create_pitch_session(
            session_id="test_session_123",
            pitch_text="This is a test pitch for our revolutionary app",
            amount_invested=50000,
            percentage_equity=15
        )
        print(f"✅ Pitch session created with ID: {pitch_session.id}")
        
        # Test adding Q&A entries
        qa_entry1 = db.add_qa_entry(
            pitch_session_id=pitch_session.id,
            shark_name="Mark Cuban",
            question="What's your revenue model?",
            answer="We use a freemium model with premium subscriptions.",
            round_number=1
        )
        print(f"✅ Q&A entry created with ID: {qa_entry1.id}")
        
        qa_entry2 = db.add_qa_entry(
            pitch_session_id=pitch_session.id,
            shark_name="Lori Greiner",
            question="How do you plan to scale?",
            answer="We're focusing on viral marketing and strategic partnerships.",
            round_number=1
        )
        print(f"✅ Q&A entry created with ID: {qa_entry2.id}")
        
        # Test retrieving conversation
        conversation = db.get_complete_conversation("test_session_123")
        if conversation:
            print("✅ Conversation retrieved successfully!")
            print(f"   Pitch: {conversation['pitch_session']['pitch_text'][:50]}...")
            print(f"   Q&A entries: {len(conversation['qa_history'])}")
        else:
            print("❌ Failed to retrieve conversation")
        
        # Cleanup
        db.close()
        print("✅ Database test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_session_manager():
    """Test session manager functionality"""
    print("\n🧪 Testing Session Manager...")
    
    try:
        session_mgr = SessionManager()
        
        # Test creating a session
        pitch_data = {
            'pitch_text': 'Test pitch for session manager',
            'amount_invested': 75000,
            'percentage_equity': 20
        }
        
        session_id = session_mgr.create_session(pitch_data)
        print(f"✅ Session created with ID: {session_id}")
        
        # Test adding Q&A rounds
        session_mgr.add_qa_round(session_id, "Kevin O'Leary", "What's your exit strategy?", "IPO or acquisition in 5-7 years")
        session_mgr.add_qa_round(session_id, "Barbara Corcoran", "Who are your competitors?", "We have 3 main competitors but our technology is superior")
        
        # Test getting session summary
        summary = session_mgr.get_session_summary(session_id)
        if summary:
            print("✅ Session summary generated successfully!")
            print(f"   Total Q&A rounds: {summary['total_qa_rounds']}")
            print(f"   Conversation length: {len(summary['conversation_summary'])} characters")
        else:
            print("❌ Failed to generate session summary")
        
        # Cleanup
        session_mgr.cleanup_session(session_id)
        print("✅ Session manager test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Session manager test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Shark Tank Database Tests...\n")
    
    success = True
    
    # Test database functionality
    if not test_database_connection():
        success = False
    
    # Test session manager
    if not test_session_manager():
        success = False
    
    print("\n" + "="*50)
    if success:
        print("🎉 All tests passed! The database integration is working correctly.")
        print("\nYou can now run the main Shark Tank application:")
        print("cd shark_tank/src")
        print("python -m shark_tank.main")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("\nCommon issues:")
        print("1. PostgreSQL is not running")
        print("2. Database connection parameters are incorrect")
        print("3. Database or tables don't exist (run setup_database.py first)")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
