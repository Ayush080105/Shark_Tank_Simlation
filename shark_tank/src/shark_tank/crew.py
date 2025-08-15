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
            ("Mark Cuban", self.shark_mark_cuban_question, self.shark_mark_cuban),
            ("Lori Greiner", self.shark_lori_greiner_question, self.shark_lori_greiner),
            ("Barbara Corcoran", self.shark_barbara_corcoran_question, self.shark_barbara_corcoran),
            ("Robert Herjavec", self.shark_robert_herjavec_question, self.shark_robert_herjavec),
            ("Kevin O'Leary", self.shark_kevin_oleary_question, self.shark_kevin_oleary),
            ("Daymond John", self.shark_daymond_john_question, self.shark_daymond_john),
        ]

        answered_sharks = set()  # Track sharks who completed Q&A

        for shark_name, task_fn, agent_fn in qa_rounds:
            question_text = agent_fn().execute_task(
                task_fn(),
                {"pitch": pitch_result}
            )
            print(f"\n🦈 {shark_name} Shark asks: {question_text}")
            human_answer = input("💬 Your answer (type 'exit' to skip to verdicts): ")

            if human_answer.strip().lower() == "exit":
                print("\n⏭️ Exiting Q&A early. Moving directly to verdicts...")
                break  # Skip directly to verdict phase

            inputs[f"{shark_name.lower().replace(' ', '_')}_answer"] = human_answer
            answered_sharks.add(shark_name)

        # Step 3: Each shark verdict
        offers = {}
        verdict_tasks = [
            ("Mark Cuban", self.shark_mark_cuban_verdict, self.shark_mark_cuban),
            ("Lori Greiner", self.shark_lori_greiner_verdict, self.shark_lori_greiner),
            ("Barbara Corcoran", self.shark_barbara_corcoran_verdict, self.shark_barbara_corcoran),
            ("Robert Herjavec", self.shark_robert_herjavec_verdict, self.shark_robert_herjavec),
            ("Kevin O'Leary", self.shark_kevin_oleary_verdict, self.shark_kevin_oleary),
            ("Daymond John", self.shark_daymond_john_verdict, self.shark_daymond_john),
        ]

        for shark_name, task_fn, agent_fn in verdict_tasks:
            if shark_name not in answered_sharks:
                offers[shark_name] = "No"  # Default verdict if no Q&A done
                print(f"\n🦈 {shark_name} Shark Verdict: No (skipped Q&A)")
            else:
                verdict = agent_fn().execute_task(task_fn(), inputs)
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
