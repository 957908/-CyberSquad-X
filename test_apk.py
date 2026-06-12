from agents.apk_agent import APKAgent

agent = APKAgent()

apk_file = input(
    "Enter APK Path: "
)

result = agent.execute(
    apk_file
)

print(result)