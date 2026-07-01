from agents.nmap_agent import NmapAgent

agent = NmapAgent()

result = agent.scan(
    "www.cdac.in"
)

print(result)