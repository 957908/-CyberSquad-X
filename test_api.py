from agents.api_agent import APIAgent
from agents.api_analysis_agent import APIAnalysisAgent

api = APIAgent()
analysis = APIAnalysisAgent()

result = api.execute(
    "https://jsonplaceholder.typicode.com/posts"
)

print(result)

print("\n")

print(
    analysis.analyze(result)
)