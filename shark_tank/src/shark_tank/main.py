#!/usr/bin/env python
import warnings
from shark_tank.crew import SharkTank

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Runs the Shark Tank simulation in interactive mode.
    """
    pitch_text = input("🗣 Please enter your pitch: ")

    inputs = {
        'pitch_text': pitch_text,
        'amount_invested': 100000,
        'percentage_equity': 10
    }

    tank = SharkTank()

    print("\n🚀 Starting Interactive Shark Tank Round...\n")
    try:
        tank.interactive_round(inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()
