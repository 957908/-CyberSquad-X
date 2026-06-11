from agents.real_cve_agent import RealCVEAgent

agent = RealCVEAgent()

results = agent.search_cve(
    "Apache"
)

for cve in results:

    print(
        f"\n{cve['id']}"
    )

    print(
        cve['description']
    )