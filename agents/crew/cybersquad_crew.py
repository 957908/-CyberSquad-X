import os
import sys

# Configure UTF-8 encoding for standard output on Windows to support emojis
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Set dummy key for CrewAI startup check if not already configured
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "not-needed"

from crewai import Agent, Task, Crew, LLM


class CyberSquadCrew:

    def run(self, target, risk_score, vulnerabilities):

        # Ollama LLM
        llm = LLM(
            model="ollama/mistral",
            base_url="http://localhost:11434"
        )

        recon_agent = Agent(
            role="Recon Specialist",
            goal="Analyze reconnaissance findings",
            backstory="Expert in attack surface analysis",
            verbose=True,
            llm=llm
        )

        risk_agent = Agent(
            role="Risk Analyst",
            goal="Evaluate cybersecurity risk",
            backstory="Expert in vulnerability assessment",
            verbose=True,
            llm=llm
        )

        advisor_agent = Agent(
            role="Security Advisor",
            goal="Provide remediation advice",
            backstory="Senior cybersecurity consultant",
            verbose=True,
            llm=llm
        )

        task1 = Task(
            description=f"""
            Analyze reconnaissance results for:
            {target}

            Vulnerabilities:
            {vulnerabilities}
            """,
            expected_output="Summary of reconnaissance findings.",
            agent=recon_agent
        )

        task2 = Task(
            description=f"""
            Evaluate risk score:
            {risk_score}/100

            Explain why this score is important.
            """,
            expected_output="Detailed risk assessment.",
            agent=risk_agent
        )

        task3 = Task(
            description="""
            Create security recommendations
            based on the findings.
            """,
            expected_output="List of security recommendations.",
            agent=advisor_agent
        )

        crew = Crew(
            agents=[
                recon_agent,
                risk_agent,
                advisor_agent
            ],
            tasks=[
                task1,
                task2,
                task3
            ],
            verbose=True
        )

        result = crew.kickoff()

        return str(result)