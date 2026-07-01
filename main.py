from datetime import datetime

from agents.website_agent import WebsiteAgent
from agents.website_analysis_agent import WebsiteAnalysisAgent
from agents.recon_agent import ReconAgent
from agents.risk_agent import RiskAgent
from agents.ai_assistant_agent import AIAssistantAgent
from agents.ollama_agent import OllamaAgent
from agents.crew.cybersquad_crew import CyberSquadCrew

from reports.report_agent import ReportAgent
from reports.json_report_agent import JSONReportAgent
from reports.pdf_report_agent import PDFReportAgent

from database.database import CyberSquadDB
from agents.nmap_agent import NmapAgent

def main():

    print("=" * 60)
    print("CyberSquad X")
    print("AI Powered Cybersecurity Platform")
    print("=" * 60)

    target = input("\nEnter Website URL: ")

    # Initialize Agents
    website_agent = WebsiteAgent()
    website_analysis_agent = WebsiteAnalysisAgent()
    recon_agent = ReconAgent()
    risk_agent = RiskAgent()
    ai_agent = AIAssistantAgent()
    ollama_agent = OllamaAgent()
    crew = CyberSquadCrew()
    nmap_agent = NmapAgent()

    # Reports
    report_agent = ReportAgent()
    json_agent = JSONReportAgent()
    pdf_agent = PDFReportAgent()

    # Database
    db = CyberSquadDB()

    # Website Scan
    website_result = website_agent.execute(target)

    print("\n" + "=" * 60)
    print("WEBSITE SCAN RESULTS")
    print("=" * 60)
    print(website_result)

    # Website Analysis
    analysis = website_analysis_agent.analyze(
        website_result
    )

    print("\n" + "=" * 60)
    print("WEBSITE SECURITY ANALYSIS")
    print("=" * 60)
    print(analysis)

    # Recon Scan
    recon_result = recon_agent.scan(target)

    print("\n" + "=" * 60)
    print("RECON RESULTS")
    print("=" * 60)
    nmap_result = nmap_agent.scan(
        target.replace(
            "https://",
            ""
        ).replace(
            "http://",
            ""
        )
    )

    print("\n")
    print("=" * 60)
    print("NMAP RESULTS")
    print("=" * 60)
    print(nmap_result)

    for path, status in recon_result.items():
        print(f"{path} -> {status}")

    # Risk Score
    score = risk_agent.calculate_risk(
        website_result,
        recon_result
    )

    print("\n" + "=" * 60)
    print("RISK SCORE")
    print("=" * 60)
    print(f"{score}/100")

    # Vulnerability Detection
    vulnerabilities = []

    if website_result.get("missing_headers"):
        vulnerabilities.append(
            "Missing Security Headers"
        )

    if recon_result.get("/admin") == 200:
        vulnerabilities.append(
            "Admin Panel Exposed"
        )

    if recon_result.get("/login") == 200:
        vulnerabilities.append(
            "Login Page Accessible"
        )

    if recon_result.get("/dashboard") == 200:
        vulnerabilities.append(
            "Dashboard Accessible"
        )

    # Ollama Analysis
    ai_analysis = ollama_agent.analyze(
        target,
        score,
        vulnerabilities
    )

    print("\n" + "=" * 60)
    print("OLLAMA AI ANALYSIS")
    print("=" * 60)
    print(ai_analysis)

    # CrewAI Analysis
    crew_analysis = crew.run(
        target,
        score,
        vulnerabilities
    )

    print("\n" + "=" * 60)
    print("CREW AI ANALYSIS")
    print("=" * 60)
    print(crew_analysis)

    # Save Database
    db.save_scan(
        target,
        score,
        str(datetime.now())
    )

    # TXT Report
    txt_file = report_agent.generate_report(
        target,
        str(website_result),
        analysis
    )

    # JSON Report
    json_agent.save(
        target,
        score,
        website_result,
        recon_result,
        vulnerabilities,
        ai_analysis,
        crew_analysis,
        nmap_result
    )

    # PDF Report
    pdf_file = pdf_agent.generate_pdf(
        target,
        score,
        analysis
    )

    print("\n" + "=" * 60)
    print("REPORTS GENERATED")
    print("=" * 60)
    print(f"TXT Report  : {txt_file}")
    print(f"PDF Report  : {pdf_file}")
    print("JSON Report : reports/latest_scan.json")

    # Rule Based Assistant
    advice = ai_agent.generate_advice(
        target,
        score,
        vulnerabilities
    )

    print("\n" + "=" * 60)
    print("AI SECURITY ASSISTANT")
    print("=" * 60)
    print(advice)


if __name__ == "__main__":
    main()