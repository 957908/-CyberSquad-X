from agents.website_agent import WebsiteAgent
from agents.website_analysis_agent import WebsiteAnalysisAgent
from agents.recon_agent import ReconAgent
from agents.risk_agent import RiskAgent
from agents.ai_assistant_agent import AIAssistantAgent

from reports.report_agent import ReportAgent
from reports.json_report_agent import JSONReportAgent

from database.database import CyberSquadDB
from reports.pdf_report_agent import PDFReportAgent
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

    ai_agent = AIAssistantAgent()
    db = CyberSquadDB()

    pdf_agent = PDFReportAgent()


    # Website Scan
    website_result = website_agent.execute(
        target
    )

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

    # Save Scan to Database
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

    # Vulnerabilities
    vulnerabilities = [
        "Missing Security Headers",
        "Open Admin Page"
    ]

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
        # Save PDF Report
    pdf_file = pdf_agent.generate_pdf(
        target,
        score,
        analysis
)

    print("\n")
    print("=" * 60)
    print("REPORTS GENERATED")
    print("=" * 60)
    print(f"TXT Report : {filename}")
    print(f"PDF Report : {pdf_file}")
    print("JSON Report: reports/latest_scan.json")

    # AI Assistant
    advice = ai_agent.generate_advice(
        target,
        score,
        vulnerabilities
    )

    print("\n")
    print("=" * 60)
    print("AI SECURITY ASSISTANT")
    print("=" * 60)
    print(advice)


if __name__ == "__main__":
    main()