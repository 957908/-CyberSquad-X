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

from scanners.windows_scanner import WindowsScanner
from scanners.adb_scanner import ADBScanner
from agents.system_analyst_agent import SystemAnalystAgent

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


# ==================================================
# Database
# ==================================================

db = CyberSquadDB()

# ==================================================
# Request Models
# ==================================================


class ScanRequest(BaseModel):
    target: str
    features: list[str] = None


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    work_organization: str
    mobile_number: str
    username: str
    password: str


class ForgotPasswordRequest(BaseModel):
    username: str
    method: str


class ForgotPasswordVerify(BaseModel):
    username: str
    otp: str
    new_password: str

@app.post("/login")
async def login(user: UserLogin):
    db_user = db.get_user(user.username)
    if not db_user:
        return {"success": False, "message": "User not found."}

    if not verify_password(user.password, db_user["password"]):
        return {"success": False, "message": "Incorrect password."}

    token = create_token({
        "username": user.username,
        "role": db_user["role"]
    })

    return {
        "success": True,
        "token": token,
        "role": db_user["role"]
    }


@app.post("/register")
async def register(user: UserRegister):
    db_user = db.get_user(user.username)
    if db_user:
        return {"success": False, "message": "Username already exists."}
    
    from api.auth.password import hash_password
    pw_hash = hash_password(user.password)
    success = db.create_user(
        user.username,
        pw_hash,
        user.first_name,
        user.last_name,
        user.work_organization,
        user.mobile_number
    )
    if success:
        return {"success": True, "message": "Registration successful."}
    else:
        return {"success": False, "message": "Failed to create user."}


# Temporary mock OTP store
mock_otps = {}


@app.post("/forgot-password/request")
async def forgot_password_request(req: ForgotPasswordRequest):
    db_user = db.get_user(req.username)
    if not db_user:
        return {"success": False, "message": "User not found."}
    
    import random
    otp = str(random.randint(100000, 999999))
    mock_otps[req.username] = otp
    
    # Simulate sending OTP
    print("=" * 60)
    print(f"MOCK SMS/EMAIL GATEWAY -> SENT TO {db_user['mobile_number'] if req.method == 'mobile' else req.username}")
    print(f"OTP CODE: {otp}")
    print("=" * 60)
    
    return {
        "success": True,
        "message": f"OTP successfully sent via {req.method}.",
        "otp_mock": otp
    }


@app.post("/forgot-password/verify")
async def forgot_password_verify(req: ForgotPasswordVerify):
    stored_otp = mock_otps.get(req.username)
    if not stored_otp or stored_otp != req.otp:
        return {"success": False, "message": "Invalid or expired OTP."}
    
    from api.auth.password import hash_password
    pw_hash = hash_password(req.new_password)
    success = db.update_password(req.username, pw_hash)
    
    if success:
        mock_otps.pop(req.username, None)
        return {"success": True, "message": "Password updated successfully."}
    else:
        return {"success": False, "message": "Failed to update password."}




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
# System & Device Scanners API
# ==================================================

@app.post("/scan-system")
async def scan_local_system():
    try:
        scanner = WindowsScanner()
        analyst = SystemAnalystAgent()
        
        report = scanner.scan()
        analysis = analyst.analyze(report, "windows")
        
        return {
            "success": True,
            "device_type": "windows",
            "report": report,
            "analysis": analysis
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/scan-android")
async def scan_connected_android():
    try:
        scanner = ADBScanner()
        analyst = SystemAnalystAgent()
        
        report = scanner.scan()
        if report.get("status") == "error":
            return {
                "success": False,
                "error": report.get("message")
            }
            
        analysis = analyst.analyze(report, "android")
        
        return {
            "success": True,
            "device_type": "android",
            "report": report,
            "analysis": analysis
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


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
        

        # Parse requested features (fallback to all if empty)
        features = request.features
        if not features:
            features = ["nmap", "subdomain", "whois", "ssl", "geoip", "cve", "owasp", "mitre", "compliance"]

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
        # Nmap & Port Intelligence
        # ----------------------------

        if "nmap" in features:
            nmap_result = nmap_agent.scan(clean_target)
            print("Nmap Scan Done")
            port_intelligence = port_agent.analyze(nmap_result)
        else:
            nmap_result = "Nmap Scan Disabled"
            port_intelligence = []

        # ----------------------------
        # Subdomains
        # ----------------------------

        if "subdomain" in features:
            subdomain_result = subdomain_agent.scan(clean_target.replace("www.", ""))
            print("Subdomain Scan Done")
        else:
            subdomain_result = []

        # ----------------------------
        # Recon Scan
        # ----------------------------

        if "owasp" in features or "mitre" in features or "compliance" in features:
            recon_result = recon_agent.scan(request.target)
            print("Recon Scan Done")
        else:
            recon_result = {}

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

        if "whois" in features:
            whois_result = whois_agent.lookup(clean_target)
            print("WHOIS Done")
        else:
            whois_result = {"status": "skipped", "message": "WHOIS Lookup Disabled"}

        # ----------------------------
        # SSL
        # ----------------------------

        if "ssl" in features:
            ssl_result = ssl_agent.scan(clean_target)
            print("SSL Done")
        else:
            ssl_result = {"ssl_enabled": False, "message": "SSL Audit Disabled"}

        # ----------------------------
        # GEO IP
        # ----------------------------

        if "geoip" in features:
            geoip_result = geoip_agent.lookup(clean_target)
            print("GeoIP Done")
        else:
            geoip_result = {"status": "skipped", "message": "GeoIP Lookup Disabled"}

        # ----------------------------
        # CVE Detection
        # ----------------------------

        if "cve" in features and "nmap" in features:
            cve_result = cve_agent.check(nmap_result)
            print("CVE Check Done")
        else:
            cve_result = []

        # ----------------------------
        # OWASP Mapping
        # ----------------------------

        if "owasp" in features:
            owasp_result = owasp_agent.map_vulnerabilities(vulnerabilities)
            print("OWASP Mapping Done")
        else:
            owasp_result = []

        # ----------------------------
        # Attack Surface & Technologies
        # ----------------------------

        attack_surface = attack_surface_agent.analyze(
            subdomain_result,
            nmap_result if "nmap" in features else "",
            vulnerabilities
        )

        technology_result = technology_agent.detect(request.target)

        # ----------------------------
        # AI Agents Analysis
        # ----------------------------

        security_analysis = security_agent.analyze(
            risk_score,
            vulnerabilities,
            cve_result
        )

        threat_result = threat_agent.hunt(
            vulnerabilities,
            cve_result,
            port_intelligence
        )

        incident_result = incident_agent.respond(
            threat_result,
            vulnerabilities
        )

        # ----------------------------
        # Compliance
        # ----------------------------

        if "compliance" in features:
            compliance_result = compliance_agent.audit(
                vulnerabilities,
                security_grade,
                ssl_result
            )
            print("Compliance Audit Done")
        else:
            compliance_result = []

        executive_report = report_writer.generate(
            request.target,
            risk_score,
            vulnerabilities,
            cve_result,
            compliance_result
        )

        mitre_result = mitre_agent.map(vulnerabilities) if "mitre" in features else []


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