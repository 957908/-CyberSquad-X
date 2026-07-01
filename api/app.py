from datetime import datetime
import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents.website_agent import WebsiteAgent
from agents.recon_agent import ReconAgent
from agents.risk_agent import RiskAgent
from agents.nmap_agent import NmapAgent
from agents.ollama_agent import OllamaAgent

from database.database import CyberSquadDB
from api.agents.whois_agent import WhoisAgent
from api.agents.ssl_agent import SSLAgent
from api.agents.geoip_agent import GeoIPAgent
from api.agents.cve_agent import CVEAgent
from api.agents.owasp_agent import OWASPAgent
from api.agents.subdomain_agent import SubdomainAgent
from api.agents.attack_surface_agent import AttackSurfaceAgent
from api.agents.technology_agent import TechnologyAgent
from api.agents.port_intelligence_agent import PortIntelligenceAgent
from api.agents.security_grade_agent import SecurityGradeAgent
from api.agents.pdf_agent import PDFAgent
from api.agents.security_analyst_agent import SecurityAnalystAgent
from api.agents.threat_hunter_agent import ThreatHunterAgent
from api.agents.incident_response_agent import IncidentResponseAgent
from api.agents.compliance_agent import ComplianceAgent
from api.agents.report_writer_agent import ReportWriterAgent
from api.agents.mitre_agent import MitreAgent
from api.models.auth import UserLogin
from api.auth.users import users
from api.auth.password import verify_password
from api.auth.jwt_handler import create_token

# ==================================================
# FastAPI Application
# ==================================================

app = FastAPI(
    title="CyberSquad X API",
    description="AI-Powered Cybersecurity Assessment Platform",
    version="2.1.0"
)

# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure reports directory exists and is mounted
os.makedirs("reports", exist_ok=True)
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

@app.post("/login")
async def login(
    user: UserLogin
):

    db_user = users.get(
        user.username
    )

    if not db_user:

        return {
            "success": False
        }

    if not verify_password(
        user.password,
        db_user["password"]
    ):

        return {
            "success": False
        }

    token = create_token({
        "username":
            user.username,

        "role":
            db_user["role"]
    })

    return {
        "success": True,
        "token": token,
        "role": db_user["role"]
    }

# ==================================================
# Database
# ==================================================

db = CyberSquadDB()

# ==================================================
# Request Model
# ==================================================


class ScanRequest(BaseModel):
    target: str


# ==================================================
# Home Route
# ==================================================

@app.get("/")
async def home():

    return {
        "status": "online",
        "application": "CyberSquad X",
        "version": "2.1.0"
    }


# ==================================================
# Scan History
# ==================================================

@app.get("/history")
async def history():

    scans = db.get_all_scans()

    return {
        "count": len(scans),
        "history": scans
    }


# ==================================================
# Latest Report
# ==================================================

@app.get("/latest-report")
async def latest_report():

    report_file = "reports/latest_scan.json"

    if not os.path.exists(report_file):

        return {
            "success": False,
            "message": "No report found"
        }

    with open(
        report_file,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==================================================
# Scan API
# ==================================================

@app.post("/scan")
async def scan_target(request: ScanRequest):

    try:

        print("=" * 60)
        print("TARGET =", request.target)

        # Agents
        website_agent = WebsiteAgent()
        recon_agent = ReconAgent()
        risk_agent = RiskAgent()
        nmap_agent = NmapAgent()
        ollama_agent = OllamaAgent()

        whois_agent = WhoisAgent()
        ssl_agent = SSLAgent()
        geoip_agent = GeoIPAgent()

        cve_agent = CVEAgent()
        owasp_agent = OWASPAgent()
        subdomain_agent = SubdomainAgent()
        attack_surface_agent = AttackSurfaceAgent()
        technology_agent =TechnologyAgent()
        port_agent = PortIntelligenceAgent()
        security_grade_agent =SecurityGradeAgent()
        pdf_agent = PDFAgent()
        security_agent = SecurityAnalystAgent()
        threat_agent = ThreatHunterAgent()
        incident_agent = IncidentResponseAgent()
        compliance_agent = ComplianceAgent()
        report_writer = ReportWriterAgent()
        mitre_agent = MitreAgent()
        
        # ------------------------
        # Website Scan
        # ----------------------------

        website_result = website_agent.execute(
            request.target
        )

        print("Website Scan Done")
        security_grade = security_grade_agent.calculate(
            website_result
        )
        print("Security Grade Calculation Done")
        

        # ----------------------------
        # Recon Scan
        # ----------------------------

        recon_result = recon_agent.scan(
            request.target
        )

        print("Recon Scan Done")

        # ----------------------------
        # Clean Target
        # ----------------------------

        clean_target = (
            request.target
            .replace("https://", "")
            .replace("http://", "")
            .split("/")[0]
        )

        print("CLEAN TARGET =", clean_target)

        # ----------------------------
        # Nmap Scan
        # ----------------------------

        nmap_result = nmap_agent.scan(
            clean_target
        )

        print("Nmap Scan Done")
        port_intelligence = port_agent.analyze(
            nmap_result
        )

        subdomain_result = subdomain_agent.scan(
            clean_target.replace("www.", "")
        )

        # ----------------------------
        # Risk Score
        # ----------------------------

        risk_score = risk_agent.calculate_risk(
            website_result,
            recon_result
        )

        # ----------------------------
        # Vulnerabilities
        # ----------------------------

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

        print(
            "Vulnerabilities =",
            vulnerabilities
        )

        # ----------------------------
        # WHOIS
        # ----------------------------

        whois_result = whois_agent.lookup(
            clean_target
        )

        # ----------------------------
        # SSL
        # ----------------------------

        ssl_result = ssl_agent.scan(
            clean_target
        )

        # ----------------------------
        # GEO IP
        # ----------------------------

        geoip_result = geoip_agent.lookup(
            clean_target
        )

        # ----------------------------
        # CVE Detection
        # ----------------------------

        cve_result = cve_agent.check(
            nmap_result
        )

        # ----------------------------
        # OWASP Mapping
        # ----------------------------

        owasp_result = (
            owasp_agent
            .map_vulnerabilities(
                vulnerabilities
            )
        )
        attack_surface = (
            attack_surface_agent.analyze(
                subdomain_result,
                nmap_result,
                vulnerabilities
            )
        )
        technology_result = (
            technology_agent.detect(
                request.target
            )
        )
        security_analysis = (
            security_agent.analyze(
                risk_score,
                vulnerabilities,
                cve_result
            )
        )
        threat_result = (
            threat_agent.hunt(
                vulnerabilities,
                cve_result,
                port_intelligence
            )
        )
        incident_result = incident_agent.respond(
            threat_result,
            vulnerabilities
        )
        compliance_result = compliance_agent.audit(
            vulnerabilities,
            security_grade,
            ssl_result
        )
        executive_report = report_writer.generate(
            request.target,
            risk_score,
            vulnerabilities,
            cve_result,
            compliance_result
        )

        mitre_result = mitre_agent.map(vulnerabilities)


        # ----------------------------
        # AI Analysis
        # ----------------------------

        ai_analysis = (
            ollama_agent.analyze(
                request.target,
                risk_score,
                vulnerabilities
            )
        )


        # ----------------------------
        # Save History
        # ----------------------------

        db.save_scan(
            request.target,
            risk_score,
            str(datetime.now())
        )

        report_data = {
            "target": request.target,
            "risk_score": risk_score,
            "security_grade": security_grade,
            "vulnerabilities": vulnerabilities,
            "cve": cve_result,
            "owasp_scan": owasp_result,
        }

        print("Returning Response")
        pdf_file = pdf_agent.generate(
            report_data
        )

        # ----------------------------
        # Response
        # ----------------------------

        return {
            "success": True,
            "target": request.target,

            "risk_score": risk_score,

            "vulnerabilities": vulnerabilities,

            "website_scan": website_result,

            "recon_scan": recon_result,

            "nmap_scan": nmap_result,

            "whois": whois_result,

            "ssl": ssl_result,
            "ssl_scan": ssl_result,

            "geoip": geoip_result,

            "cve": cve_result,
            "cve_scan": cve_result,

            "owasp_scan": owasp_result,

            "ai_analysis": ai_analysis,
            "subdomain_scan": subdomain_result,
            "attack_surface": attack_surface,
            "technology_scan": technology_result,
            "technologies": technology_result,
            "port_intelligence": port_intelligence,
            "security_grade": security_grade,
            "pdf_report": pdf_file,
            "mitre": mitre_result,
            "security_analysis": security_analysis,
            "threat_hunting": threat_result,
            "incident_response": incident_result,
            "compliance_audit": compliance_result,
            "compliance": compliance_result,
            "executive_report": executive_report
        }

    except Exception as e:

        print(
            "ERROR =",
            str(e)
        )

        return {
            "success": False,
            "error": str(e)
        }