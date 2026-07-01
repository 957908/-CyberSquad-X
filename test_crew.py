from agents.crew.cybersquad_crew import CyberSquadCrew

crew = CyberSquadCrew()

result = crew.run(
    "https://www.cdac.in",
    60,
    [
        "Admin Panel Exposed",
        "Dashboard Accessible"
    ]
)

print(result)