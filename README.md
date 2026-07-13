# 🛡️ CyberSquad X
### *AI-Powered Cybersecurity Operations & Assessment Platform*

![CyberSquad X Dashboard Console](dashboard_screenshot.png)

CyberSquad X is a modern, state-of-the-art cybersecurity analysis platform that automates attack surface discovery, scans target networks, checks SSL/WHOIS info, maps vulnerabilities to **OWASP Top 10** and **MITRE ATT&CK** frameworks, performs local hardware diagnostics, and generates detailed security compliance audits using **local AI Agents** (Ollama/CrewAI).

---

## 🚀 Key Features

- **🌐 Comprehensive Target Scanning**: Performs quick directory audits, port mapping (via Nmap), subdomain discovery, SSL certificate audits, and WHOIS lookups.
- **⚙️ Selective Scanning Grid**: Choose exactly which scanning modules to run (*Nmap, Subdomains, WHOIS, SSL, GeoIP, CVE, OWASP, MITRE, Compliance*) to optimize execution speed.
- **💻 Hardware Diagnostics (Local & Mobile)**:
  - **Local Windows OS Audit**: Audits Windows Defender states, active firewall profiles, active TCP listener ports, and system hotfixes using native PowerShell scripts.
  - **Android USB Cable Audit**: Communicates with connected Android devices over USB using **ADB (Android Debug Bridge)** to audit USB Debugging status, sideloading configurations, mock locations, and installed third-party apps.
- **👥 Multi-Agent Security Analysis**: Integrates **CrewAI** and **Ollama** agents (using local models like `mistral`) to analyze risks, calculate scores, and write executive security reports.
- **☀️ Light / 🌙 Dark Theme**: Transition the entire Security Console from a cyberpunk dark layout to a premium light theme with a single click.
- **📄 Executive PDF Reporting**: Instantly compiles and downloads security assessment results into high-quality PDF reports.
- **🔒 Persistent Database & Registration**: Uses SQLite (`cybersquad.db`) to manage user registration, hash passwords securely, and store historical scan logs.

---

## 📐 System Workflow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as Operator (Browser)
    participant Front as React Frontend (GitHub Pages)
    participant Back as FastAPI Backend (Localhost)
    participant DB as SQLite Database
    participant Scanners as Scanning Modules
    participant AI as AI Specialist Agents (Ollama)
    
    %% Registration and Login
    User->>Front: Access portal, register or request login
    Front->>Back: POST /login (credentials)
    Back->>DB: Query user hash
    DB-->>Back: User hash match
    Back-->>Front: JWT Token (admin/analyst/viewer role)
    
    %% Target Security Audit
    User->>Front: Enter target domain + check selective features + click Initiate Audit
    Front->>Back: POST /scan {target, features}
    activate Back
    Note over Back: Parse requested modules (Nmap, SSL, Subdomain...)
    Back->>Scanners: Trigger selective scanners
    Scanners-->>Back: Scan results telemetry
    Back->>AI: Send telemetry to security analyst agents
    AI-->>Back: Mitigation advisories & CVE mappings
    Back->>DB: Log scan history
    Back-->>Front: JSON scan report data
    deactivate Back
    Front-->>User: Render interactive dashboard cards, charts & download PDF report
    
    %% Hardware Telemetry Scan
    User->>Front: Click Run Diagnostics Audit (Windows/Android)
    Front->>Back: POST /scan-system or /scan-android
    activate Back
    alt Windows OS Selected
        Back->>Scanners: Run PowerShell diagnostics
    else Android USB Selected
        Back->>Scanners: Query ADB shell tools (via local platform-tools)
    end
    Scanners-->>Back: Telemetry (Antivirus, Firewall, USB Debugging...)
    Back->>AI: Analyze hardware state (Mistral AI)
    AI-->>Back: Security advisories
    Back-->>Front: JSON device report
    deactivate Back
    Front-->>User: Render audit logs & advisory checklist
```

---

## 🛠️ Project Structure

```
├── agents/                  # Local scanners and crewAI flows
│   ├── crew/
│   │   └── cybersquad_crew.py # CrewAI multi-agent definition
│   ├── system_analyst_agent.py # Analyzes local/mobile telemetry using Ollama
│   ├── nmap_agent.py        # Wrapper for Nmap network commands
│   └── ollama_agent.py      # Local Ollama AI client wrapper
├── api/                     # Backend FastAPI application
│   ├── agents/              # Modular security analytical agents
│   │   ├── compliance_agent.py   # Audits NIST/ISO/OWASP controls
│   │   ├── mitre_agent.py        # Maps issues to MITRE ATT&CK
│   │   └── ssl_agent.py          # Performs certificate verification
│   ├── auth/                # JWT and authentication helpers
│   ├── models/              # Pydantic request & response models
│   └── app.py               # Main API application entrypoint
├── cybersquad-frontend/     # Modern React + Vite frontend console
│   ├── src/
│   │   ├── components/      # Sidebar, Navbar, Charts, and gauges
│   │   └── pages/           # Dashboard, Login, and Admin screens
├── database/                # SQLite local storage driver
├── scanners/                # Hardware level scanners
│   ├── adb_scanner.py       # Communicates with Android via ADB
│   └── windows_scanner.py   # System audit using PowerShell cmdlets
└── platform-tools-latest-windows/ # Optional: Local adb platform-tools
```

---

## 📦 Local Installation & Setup

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Nmap** (must be added to your system's PATH)
- **Ollama** (running locally with `mistral` pulled: `ollama pull mistral`)
- **ADB Tools** (Optional - if scanning Android over USB. The scanner automatically checks for a `platform-tools` folder inside your project directory).

### 1. Backend Setup
1. Navigate to the root directory:
   ```bash
   cd cybersquad
   ```
2. Install python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the API server:
   ```bash
   python -m uvicorn api.app:app --host 127.0.0.1 --port 8000
   ```

### 2. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd cybersquad-frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the local Vite development server:
   ```bash
   npm run dev
   ```
4. Access the web dashboard at **`http://localhost:5173/-CyberSquad-X/`**.

---

## 🔑 Access Credentials

To log in to the Security Console, use the following default credentials:

| Identity | Cryptokey (Password) | Role |
| :--- | :--- | :--- |
| `admin` | `admin123` | **Administrator** |
| `analyst` | `analyst123` | **Security Analyst** |
| `viewer` | `viewer123` | **Guest Observer** |

---

## 🛡️ License

This project is licensed under the MIT License.
