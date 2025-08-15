#!/usr/bin/env python
import warnings
from shark_tank.crew import SharkTank

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Runs the Shark Tank simulation in interactive mode.
    """
    print("🦈 Welcome to Shark Tank!")
    print("=" * 50)
    
    # Ask if user wants to continue with existing session
    print("\n📋 Session Options:")
    print("1. Start new session (default)")
    print("2. Continue with existing session ID")
    print("3. Refresh existing session (keep pitch, reset Q&A)")
    
    choice = input("\nSelect option (1-3) or press Enter for new session: ").strip()
    
    session_id = None
    refresh_mode = False
    
    if choice == "2":
        # Continue with existing session
        session_id = input("Enter existing session ID: ").strip()
        if not session_id:
            print("⚠️  No session ID provided, starting new session...")
            session_id = None
        else:
            print(f"🔄 Continuing with session: {session_id}")
    
    elif choice == "3":
        # Refresh existing session
        session_id = input("Enter session ID to refresh: ").strip()
        if not session_id:
            print("⚠️  No session ID provided, starting new session...")
            session_id = None
        else:
            refresh_mode = True
            print(f"🔄 Refreshing session: {session_id}")
    
    else:
        print("🚀 Starting new session...")
    
    # Get pitch details
    print("\n" + "=" * 50)
    pitch_text = input("🗣 Please enter your pitch: ")
    
    if not pitch_text.strip():
        print("❌ Pitch cannot be empty. Exiting...")
        return

    inputs = {
        'pitch_text': pitch_text,
        'amount_invested': 100000,
        'percentage_equity': 10,
        'session_id': session_id,
        'refresh_mode': refresh_mode
    }

    # Ask for investment details
    try:
        amount_input = input("💰 Investment amount (default: $100,000): ").strip()
        if amount_input:
            inputs['amount_invested'] = int(amount_input.replace('$', '').replace(',', ''))
        
        equity_input = input("📊 Equity percentage (default: 10%): ").strip()
        if equity_input:
            inputs['percentage_equity'] = int(equity_input.replace('%', ''))
    except ValueError:
        print("⚠️  Invalid input, using default values...")

    tank = SharkTank()

    print("\n🚀 Starting Interactive Shark Tank Round...\n")
    try:
        tank.interactive_round(inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()
