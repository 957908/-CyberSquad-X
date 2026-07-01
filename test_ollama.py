from agents.ollama_agent import OllamaAgent

agent = OllamaAgent()

result = agent.analyze(
    "https://www.cdac.in",
    60,
    [
        "Missing Security Headers",
        "Open Admin Page"
    ]
)

print(result)