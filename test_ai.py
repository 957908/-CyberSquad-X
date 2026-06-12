from agents.ai_assistant_agent import AIAssistantAgent

ai = AIAssistantAgent()

print(
    ai.generate_advice(
        "https://www.cdac.in",
        60,
        ["Missing Headers"]
    )
)