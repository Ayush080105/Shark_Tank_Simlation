# src/shark_tank/crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class SharkTank:
    """Shark Tank crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # --- Agents ---
    @agent
    def entrepreneur_user(self) -> Agent:
        return Agent(config=self.agents_config['entrepreneur_user'], verbose=True)

    @agent
    def shark_tech(self) -> Agent:
        return Agent(config=self.agents_config['shark_tech'], verbose=True)

    @agent
    def shark_finance(self) -> Agent:
        return Agent(config=self.agents_config['shark_finance'], verbose=True)

    @agent
    def shark_marketing(self) -> Agent:
        return Agent(config=self.agents_config['shark_marketing'], verbose=True)

    @agent
    def moderator(self) -> Agent:
        return Agent(config=self.agents_config['moderator'], verbose=True)

    # --- Tasks ---
    @task
    def pitch_task(self) -> Task:
        return Task(config=self.tasks_config['pitch_task'])

    @task
    def shark_tech_question(self) -> Task:
        return Task(config=self.tasks_config['shark_tech_question'])

    @task
    def shark_finance_question(self) -> Task:
        return Task(config=self.tasks_config['shark_finance_question'])

    @task
    def shark_marketing_question(self) -> Task:
        return Task(config=self.tasks_config['shark_marketing_question'])

    @task
    def shark_tech_verdict(self) -> Task:
        return Task(config=self.tasks_config['shark_tech_verdict'])

    @task
    def shark_finance_verdict(self) -> Task:
        return Task(config=self.tasks_config['shark_finance_verdict'])

    @task
    def shark_marketing_verdict(self) -> Task:
        return Task(config=self.tasks_config['shark_marketing_verdict'])

    @task
    def moderator_summary(self) -> Task:
        return Task(config=self.tasks_config['moderator_summary'])

    # --- Interactive Q&A runner ---
    def interactive_round(self, inputs):
        print("\n🚀 Starting Interactive Shark Tank Round...")

        # Step 1: Pitch
        pitch_result = self.entrepreneur_user().execute_task(
            self.pitch_task(),
            inputs
        )
        print(f"\n🎤 Pitch Result: {pitch_result}")

        # Step 2: Sharks ask & founder answers
        qa_rounds = [
            ("Tech", self.shark_tech_question, self.shark_tech),
            ("Finance", self.shark_finance_question, self.shark_finance),
            ("Marketing", self.shark_marketing_question, self.shark_marketing),
        ]

        for shark_name, task_fn, agent_fn in qa_rounds:
            question_text = agent_fn().execute_task(
                task_fn(),
                {"pitch": pitch_result}
            )
            print(f"\n🦈 {shark_name} Shark asks: {question_text}")
            human_answer = input("💬 Your answer: ")
            inputs[f"{shark_name.lower()}_answer"] = human_answer

        # Step 3: Each shark verdict
        offers = {}
        verdict_tasks = [
            ("Tech", self.shark_tech_verdict, self.shark_tech),
            ("Finance", self.shark_finance_verdict, self.shark_finance),
            ("Marketing", self.shark_marketing_verdict, self.shark_marketing),
        ]
        for shark_name, task_fn, agent_fn in verdict_tasks:
            verdict = agent_fn().execute_task(
                task_fn(),
                inputs
            )
            offers[shark_name] = verdict
            print(f"\n🦈 {shark_name} Shark Verdict: {verdict}")

        # Step 4: Moderator summary
        inputs["offers"] = offers
        verdict_output = self.moderator().execute_task(
            self.moderator_summary(),
            inputs
        )
        print("\n📢 Final Recap:")
        print(verdict_output)

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
