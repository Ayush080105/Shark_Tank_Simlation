# src/shark_tank/crew.py

import os
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .database import DatabaseManager
from .session_manager import SessionManager

@CrewBase
class SharkTank:
    """Shark Tank crew with PostgreSQL storage"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        """Initialize SharkTank with database and session management"""
        # Initialize database manager
        self.db_manager = DatabaseManager()
        
        # Initialize session manager
        self.session_manager = SessionManager()
        
        # Load configurations
        self._load_configs()

    def _load_configs(self):
        """Load configuration files safely with UTF-8"""
        config_dir = os.path.join(os.path.dirname(__file__), 'config')
        
        # Load agents config
        agents_path = os.path.join(config_dir, 'agents.yaml')
        with open(agents_path, 'r', encoding='utf-8') as f:
            self.agents_config = yaml.safe_load(f)
        
        # Load tasks config
        tasks_path = os.path.join(config_dir, 'tasks.yaml')
        with open(tasks_path, 'r', encoding='utf-8') as f:
            self.tasks_config = yaml.safe_load(f)

    # --- Agents ---
    @agent
    def entrepreneur_user(self) -> Agent:
        return Agent(config=self.agents_config['entrepreneur_user'], verbose=True)

    @agent
    def shark_mark_cuban(self) -> Agent:
        return Agent(config=self.agents_config['shark_mark_cuban'], verbose=True)

    @agent
    def shark_lori_greiner(self) -> Agent:
        return Agent(config=self.agents_config['shark_lori_greiner'], verbose=True)

    @agent
    def shark_barbara_corcoran(self) -> Agent:
        return Agent(config=self.agents_config['shark_barbara_corcoran'], verbose=True)

    @agent
    def shark_robert_herjavec(self) -> Agent:
        return Agent(config=self.agents_config['shark_robert_herjavec'], verbose=True)

    @agent
    def shark_kevin_oleary(self) -> Agent:
        return Agent(config=self.agents_config['shark_kevin_oleary'], verbose=True)

    @agent
    def shark_daymond_john(self) -> Agent:
        return Agent(config=self.agents_config['shark_daymond_john'], verbose=True)

    @agent
    def moderator(self) -> Agent:
        return Agent(config=self.agents_config['moderator'], verbose=True)

    # --- Tasks ---
    @task
    def pitch_task(self) -> Task:
        return Task(config=self.tasks_config['pitch_task'])

    @task
    def shark_mark_cuban_question(self) -> Task:
        return Task(config=self.tasks_config['shark_mark_cuban_qna'])

    @task
    def shark_lori_greiner_question(self) -> Task:
        return Task(config=self.tasks_config['shark_lori_greiner_qna'])

    @task
    def shark_barbara_corcoran_question(self) -> Task:
        return Task(config=self.tasks_config['shark_barbara_corcoran_qna'])

    @task
    def shark_robert_herjavec_question(self) -> Task:
        return Task(config=self.tasks_config['shark_robert_herjavec_qna'])

    @task
    def shark_kevin_oleary_question(self) -> Task:
        return Task(config=self.tasks_config['shark_kevin_oleary_qna'])

    @task
    def shark_daymond_john_question(self) -> Task:
        return Task(config=self.tasks_config['shark_daymond_john_qna'])

    @task
    def shark_mark_cuban_verdict(self) -> Task:
        return Task(config=self.tasks_config['shark_mark_cuban_verdict'])

    @task
    def shark_lori_greiner_verdict(self) -> Task:
        return Task(config=self.tasks_config['shark_lori_greiner_verdict'])

    @task
    def shark_barbara_corcoran_verdict(self) -> Task:
        return Task(config=self.tasks_config['shark_barbara_corcoran_verdict'])

    @task
    def shark_robert_herjavec_verdict(self) -> Task:
        return Task(config=self.tasks_config['shark_robert_herjavec_verdict'])

    @task
    def shark_kevin_oleary_verdict(self) -> Task:
        return Task(config=self.tasks_config['shark_kevin_oleary_verdict'])

    @task
    def shark_daymond_john_verdict(self) -> Task:
        return Task(config=self.tasks_config['shark_daymond_john_verdict'])

    @task
    def moderator_summary(self) -> Task:
        return Task(config=self.tasks_config['moderator_summary'])

    def show_session_help(self):
        """Show help for session management commands"""
        print("\n📋 Session Management Commands:")
        print("  'refresh' - Refresh current session (keep pitch, reset Q&A)")
        print("  'reset' - Reset completely to session 1")
        print("  'sessions' - Show all active sessions")
        print("  'stats' - Show session statistics")
        print("  'help' - Show this help message")
        print("  'exit' - Exit Q&A and go to verdicts")

    def handle_session_command(self, command: str, current_session_id: str, inputs: dict) -> tuple:
        """Handle session management commands"""
        command = command.strip().lower()
        
        if command == 'refresh':
            try:
                new_session_id = self.session_manager.refresh_session(current_session_id)
                print(f"🔄 Session refreshed! New session ID: {new_session_id}")
                print("📝 Keeping original pitch, starting fresh Q&A...")
                return new_session_id, True  # True means continue with new session
            except ValueError as e:
                print(f"❌ Error refreshing session: {e}")
                return current_session_id, False
        
        elif command == 'reset':
            try:
                new_session_id = self.session_manager.reset_to_session_1()
                print(f"🔄 Reset to session 1! New session ID: {new_session_id}")
                print("📝 Starting completely fresh...")
                return new_session_id, True  # True means continue with new session
            except Exception as e:
                print(f"❌ Error resetting sessions: {e}")
                return current_session_id, False
        
        elif command == 'sessions':
            sessions = self.session_manager.list_active_sessions()
            if sessions:
                print("\n📊 Active Sessions:")
                for session in sessions:
                    print(f"  Session #{session['session_number']}: {session['pitch_text']}")
                    print(f"    ID: {session['session_id'][:8]}... | Created: {session['created_at']}")
            else:
                print("📊 No active sessions")
            return current_session_id, False
        
        elif command == 'stats':
            stats = self.session_manager.get_session_stats()
            print(f"\n📈 Session Statistics:")
            print(f"  Total active sessions: {stats['total_active_sessions']}")
            print(f"  Total Q&A rounds: {stats['total_qa_rounds']}")
            print(f"  Next session number: {stats['next_session_number']}")
            return current_session_id, False
        
        elif command == 'help':
            self.show_session_help()
            return current_session_id, False
        
        else:
            return current_session_id, False

    # --- Interactive Q&A runner with database storage ---
    def interactive_round(self, inputs):
        print("\n🚀 Starting Interactive Shark Tank Round...")

        # Handle session management based on user input
        session_id = inputs.get('session_id')
        refresh_mode = inputs.get('refresh_mode', False)
        
        if session_id and refresh_mode:
            # User wants to refresh a specific session
            print(f"🔄 Refreshing session: {session_id}")
            session_id = self.session_manager.refresh_session_by_id(session_id, inputs)
            print(f"✅ Session refreshed! New session ID: {session_id}")
            
        elif session_id:
            # User wants to continue with existing session
            print(f"🔄 Continuing with session: {session_id}")
            session_id = self.session_manager.continue_session(session_id, inputs)
            
        else:
            # Create a new session
            session_id = self.session_manager.create_session(inputs)
            print(f"📝 New session created with ID: {session_id}")

        # Get session info for display
        session_info = self.session_manager.get_session(session_id)
        if session_info:
            print(f"📝 Session #{session_info['session_number']} - {session_id}")

        # Store pitch in database
        try:
            pitch_session = self.db_manager.create_pitch_session(
                session_id=session_id,
                pitch_text=inputs['pitch_text'],
                amount_invested=inputs['amount_invested'],
                percentage_equity=inputs['percentage_equity']
            )
            print(f"💾 Pitch stored in database with ID: {pitch_session.id}")
        except Exception as e:
            print(f"⚠️ Warning: Failed to store pitch in database: {e}")
            print("Continuing with in-memory session only...")

        # Step 1: Pitch
        pitch_result = self.entrepreneur_user().execute_task(
            self.pitch_task(),
            inputs
        )
        print(f"\n🎤 Pitch Result: {pitch_result}")

        # Show session management help
        self.show_session_help()

        # Step 2: Sharks ask & founder answers
        qa_rounds = [
            ("Mark Cuban", self.shark_mark_cuban_question, self.shark_mark_cuban),
            ("Lori Greiner", self.shark_lori_greiner_question, self.shark_lori_greiner),
            ("Barbara Corcoran", self.shark_barbara_corcoran_question, self.shark_barbara_corcoran),
            ("Robert Herjavec", self.shark_robert_herjavec_question, self.shark_robert_herjavec),
            ("Kevin O'Leary", self.shark_kevin_oleary_question, self.shark_kevin_oleary),
            ("Daymond John", self.shark_daymond_john_question, self.shark_daymond_john),
        ]

        answered_sharks = set()
        current_round = 1

        while True:
            for shark_name, task_fn, agent_fn in qa_rounds:
                question_text = agent_fn().execute_task(
                    task_fn(),
                    {"pitch": pitch_result}
                )
                print(f"\n🦈 {shark_name} Shark asks: {question_text}")
                human_answer = input("💬 Your answer (type 'help' for commands): ")

                # Check for session management commands
                if human_answer.strip().lower() in ['refresh', 'reset', 'sessions', 'stats', 'help']:
                    new_session_id, should_continue = self.handle_session_command(
                        human_answer.strip().lower(), session_id, inputs
                    )
                    if should_continue:
                        # Update session_id and continue with new session
                        session_id = new_session_id
                        answered_sharks.clear()
                        current_round = 1
                        print(f"\n🔄 Continuing with new session: {session_id}")
                        continue
                    else:
                        # Command handled, continue with current Q&A
                        continue

                if human_answer.strip().lower() == "exit":
                    print("\n⏭️ Exiting Q&A early. Moving directly to verdicts...")
                    break

                # Store Q&A in session manager
                self.session_manager.add_qa_round(session_id, shark_name, question_text, human_answer)
                
                # Store Q&A in database
                try:
                    if 'pitch_session' in locals():
                        self.db_manager.add_qa_entry(
                            pitch_session_id=pitch_session.id,
                            shark_name=shark_name,
                            question=question_text,
                            answer=human_answer,
                            round_number=current_round
                        )
                        print(f"💾 Q&A stored in database for {shark_name}")
                except Exception as e:
                    print(f"⚠️ Warning: Failed to store Q&A in database: {e}")

                inputs[f"{shark_name.lower().replace(' ', '_')}_answer"] = human_answer
                answered_sharks.add(shark_name)

            else:
                current_round += 1
                continue
            break

        # Step 3: Verdicts
        offers = {}
        verdict_tasks = [
            ("Mark Cuban", self.shark_mark_cuban_verdict, self.shark_mark_cuban),
            ("Lori Greiner", self.shark_lori_greiner_verdict, self.shark_lori_greiner),
            ("Barbara Corcoran", self.shark_barbara_corcoran_verdict, self.shark_barbara_corcoran),
            ("Robert Herjavec", self.shark_robert_herjavec_verdict, self.shark_robert_herjavec),
            ("Kevin O'Leary", self.shark_kevin_oleary_verdict, self.shark_kevin_oleary),
            ("Daymond John", self.shark_daymond_john_verdict, self.shark_daymond_john),
        ]

        conversation_summary = self.session_manager.get_session_summary(session_id)
        
        for shark_name, task_fn, agent_fn in verdict_tasks:
            if shark_name not in answered_sharks:
                offers[shark_name] = "No"
                print(f"\n🦈 {shark_name} Shark Verdict: No (skipped Q&A)")
            else:
                verdict_inputs = {
                    **inputs,
                    'conversation_summary': conversation_summary['conversation_summary'],
                    'total_qa_rounds': conversation_summary['total_qa_rounds'],
                    'session_id': session_id
                }
                
                verdict = agent_fn().execute_task(task_fn(), verdict_inputs)
                offers[shark_name] = verdict
                print(f"\n🦈 {shark_name} Shark Verdict: {verdict}")

        # Step 4: Moderator Summary
        inputs["offers"] = offers
        inputs["conversation_summary"] = conversation_summary['conversation_summary']
        inputs["session_id"] = session_id
        
        verdict_output = self.moderator().execute_task(
            self.moderator_summary(),
            inputs
        )
        print("\n📢 Final Recap:")
        print(verdict_output)

        # Cleanup
        self.session_manager.cleanup_session(session_id)
        self.db_manager.close()

    # --- Crew definition for normal auto mode ---
    @crew
    def crew(self) -> Crew:
        """Creates the Shark Tank crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
