from agents.scanner_agent import ScannerAgent
from agents.analyst_agent import AnalystAgent
from agents.cve_agent import CVEAgent
from agents.website_agent import WebsiteAgent
from agents.website_analysis_agent import WebsiteAnalysisAgent
from agents.recon_agent import ReconAgent
from agents.risk_agent import RiskAgent

from reports.report_agent import ReportAgent
from reports.json_report_agent import JSONReportAgent

from database.database import CyberSquadDB
from datetime import datetime
def main():

    print("=" * 60)
    print("CyberSquad X")
    print("AI Powered Cybersecurity Platform")
    print("=" * 60)

    target = input("\nEnter Website URL: ")

    # Agents
    website_agent = WebsiteAgent()
    website_analysis_agent = WebsiteAnalysisAgent()
    recon_agent = ReconAgent()
    risk_agent = RiskAgent()
    report_agent = ReportAgent()
    json_agent = JSONReportAgent()
    db = CyberSquadDB()
    # Website Scan
    website_result = website_agent.execute(target)

    print("\n")
    print("=" * 60)
    print("WEBSITE SCAN RESULTS")
    print("=" * 60)
    print(website_result)

    # Website Analysis
    analysis = website_analysis_agent.analyze(
        website_result
    )

    print("\n")
    print("=" * 60)
    print("WEBSITE SECURITY ANALYSIS")
    print("=" * 60)
    print(analysis)

    # Recon Scan
    recon_result = recon_agent.scan(
        target
    )

    print("\n")
    print("=" * 60)
    print("RECON RESULTS")
    print("=" * 60)

    for path, status in recon_result.items():
        print(f"{path} -> {status}")

    # Risk Score
    score = risk_agent.calculate_risk(
        website_result,
        recon_result
    )
    db.save_scan(
    target,
    score,
    str(datetime.now())
)

    print("\n")
    print("=" * 60)
    print("RISK SCORE")
    print("=" * 60)
    print(f"{score}/100")

    # Temporary Vulnerability List
    vulnerabilities = [
        {
            "service": "Website Headers",
            "risk": "Medium"
        }
    ]
    print(type(report_agent))
    print(dir(report_agent))
    # Save TXT Report
    filename = report_agent.generate_report(
        target,
        str(website_result),
        analysis
    )

    # Save JSON Report
    json_agent.save(
        target,
        score,
        website_result,
        recon_result,
        vulnerabilities
    )


    print("\n")
    print("=" * 60)
    print("REPORTS GENERATED")
    print("=" * 60)
    print(f"TXT Report : {filename}")
    print("JSON Report: reports/latest_scan.json")
    


if __name__ == "__main__":
    main()