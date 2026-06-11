from agents.website_agent import WebsiteAgent
from agents.recon_agent import ReconAgent
from agents.risk_agent import RiskAgent

website = WebsiteAgent()
recon = ReconAgent()
risk = RiskAgent()

website_result = website.execute(
    "https://example.com"
)

recon_result = recon.scan(
    "https://example.com"
)

score = risk.calculate_risk(
    website_result,
    recon_result
)

print(
    f"Overall Risk Score: {score}/100"
)