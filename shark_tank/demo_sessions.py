#!/usr/bin/env python
"""
Demo script for Shark Tank Session Management
Shows how sessions work with refresh and reset capabilities
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from shark_tank.session_manager import SessionManager

def demo_session_management():
    """Demonstrate session management features"""
    print("🚀 Shark Tank Session Management Demo")
    print("=" * 60)
    
    # Initialize session manager
    session_mgr = SessionManager()
    
    # Demo 1: Create initial session
    print("\n📝 Demo 1: Creating initial session")
    pitch_data = {
        'pitch_text': 'Our revolutionary AI-powered app for entrepreneurs',
        'amount_invested': 100000,
        'percentage_equity': 15
    }
    
    session_id = session_mgr.create_session(pitch_data)
    print(f"✅ Session created: {session_id}")
    print(f"   Session number: #{session_mgr.get_session(session_id)['session_number']}")
    
    # Demo 2: Add some Q&A rounds
    print("\n📝 Demo 2: Adding Q&A rounds")
    session_mgr.add_qa_round(session_id, "Mark Cuban", "What's your revenue model?", "Freemium with premium subscriptions")
    session_mgr.add_qa_round(session_id, "Lori Greiner", "How do you plan to scale?", "Viral marketing and partnerships")
    
    summary = session_mgr.get_session_summary(session_id)
    print(f"✅ Added {summary['total_qa_rounds']} Q&A rounds")
    
    # Demo 3: Refresh session (keep pitch, reset Q&A)
    print("\n📝 Demo 3: Refreshing session")
    print("   This keeps the pitch but resets Q&A to round 1")
    
    new_session_id = session_mgr.refresh_session(session_id)
    print(f"✅ Session refreshed: {new_session_id}")
    print(f"   New session number: #{session_mgr.get_session(new_session_id)['session_number']}")
    
    # Show that Q&A is reset
    new_summary = session_mgr.get_session_summary(new_session_id)
    print(f"   Q&A rounds after refresh: {new_summary['total_qa_rounds']}")
    
    # Demo 4: Add new Q&A to refreshed session
    print("\n📝 Demo 4: Adding new Q&A to refreshed session")
    session_mgr.add_qa_round(new_session_id, "Kevin O'Leary", "What's your exit strategy?", "IPO in 5-7 years")
    
    final_summary = session_mgr.get_session_summary(new_session_id)
    print(f"✅ New Q&A added: {final_summary['total_qa_rounds']} rounds total")
    
    # Demo 5: Show session statistics
    print("\n📝 Demo 5: Session statistics")
    stats = session_mgr.get_session_stats()
    print(f"   Total active sessions: {stats['total_active_sessions']}")
    print(f"   Total Q&A rounds: {stats['total_qa_rounds']}")
    print(f"   Next session number: {stats['next_session_number']}")
    
    # Demo 6: Reset to session 1
    print("\n📝 Demo 6: Resetting to session 1")
    print("   This clears ALL sessions and starts fresh")
    
    fresh_session_id = session_mgr.reset_to_session_1()
    print(f"✅ Reset complete: {fresh_session_id}")
    print(f"   New session number: #{session_mgr.get_session(fresh_session_id)['session_number']}")
    
    # Final statistics
    final_stats = session_mgr.get_session_stats()
    print(f"   Sessions after reset: {final_stats['total_active_sessions']}")
    
    print("\n🎉 Demo completed!")
    print("\nKey Features Demonstrated:")
    print("  ✅ Session creation with sequential numbering")
    print("  ✅ Q&A round tracking")
    print("  ✅ Session refresh (keep pitch, reset Q&A)")
    print("  ✅ Complete reset to session 1")
    print("  ✅ Session statistics and management")
    
    # Cleanup
    session_mgr.cleanup_session(fresh_session_id)

def main():
    """Main demo function"""
    try:
        demo_session_management()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
