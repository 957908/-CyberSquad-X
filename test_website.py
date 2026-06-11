from agents.website_agent import WebsiteAgent
from agents.website_analysis_agent import WebsiteAnalysisAgent

website = WebsiteAgent()
analysis = WebsiteAnalysisAgent()

result = website.execute(
    "https://example.com"
)

report = analysis.analyze(
    result
)

print(report)