from agents.recon_agent import ReconAgent

agent = ReconAgent()

result = agent.scan(
    "https://example.com"
)

print(result)