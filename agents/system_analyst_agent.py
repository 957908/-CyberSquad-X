import ollama

class SystemAnalystAgent:

    def analyze(self, report, device_type):
        if device_type == "windows":
            prompt = f"""
You are a windows security expert. Analyze the following Windows OS security audit report:

{report}

Provide output in this format:

### Security Risks
- list risk items with bullet points (e.g. firewall disabled, Defender status, dangerous open ports)

### Impact
- explain what an attacker can do (e.g. local privilege escalation, network intrusion)

### Actionable Remediation Checklist
- step-by-step instructions to fix the issues

Keep the response under 250 words.
"""
        else: # Android
            prompt = f"""
You are an Android OS mobile security expert. Analyze the following Android USB security audit report:

{report}

Provide output in this format:

### Security Risks
- list risk items with bullet points (e.g. developer options left on, sideloading enabled, mock locations allowed, suspicious apps count)

### Impact
- explain mobile specific impacts (e.g. banking trojans, device hijacking, data theft)

### Actionable Remediation Checklist
- step-by-step instructions to secure the Android device

Keep the response under 250 words.
"""

        try:
            response = ollama.chat(
                model="mistral",
                messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]
        except Exception as e:
            # Fallback Rule-Based Advice
            return self._fallback_advice(report, device_type)

    def _fallback_advice(self, report, device_type):
        if device_type == "windows":
            advice = "### Security Risks\n"
            defender = report.get("defender", {})
            if defender.get("AntivirusEnabled") != True:
                advice += "- ⚠️ Windows Defender Antivirus might be disabled.\n"
            if defender.get("RealTimeProtectionEnabled") != True:
                advice += "- ⚠️ Real-time protection is disabled.\n"
            
            firewall = report.get("firewall", [])
            if isinstance(firewall, list):
                disabled_fw = [f.get("Name") for f in firewall if f.get("Enabled") != True]
                if disabled_fw:
                    advice += f"- ⚠️ Firewall is disabled for profiles: {', '.join(disabled_fw)}.\n"
            else:
                advice += "- ⚠️ Unable to verify firewall status.\n"
                
            open_ports = report.get("open_ports", [])
            if len(open_ports) > 5:
                advice += f"- ⚠️ High count of active listener ports ({len(open_ports)} ports active).\n"
            
            advice += "\n### Impact\n- Inactive firewalls and antivirus engines allow malicious payloads to run and expose system ports to local network scanning and remote exploitation.\n"
            advice += "\n### Actionable Remediation Checklist\n1. Open Settings -> Windows Security and enable Virus & threat protection.\n2. Open Control Panel -> Windows Defender Firewall and turn on firewall for all profiles.\n3. Close unnecessary background services to secure listener ports.\n"
            return advice
        else:
            advice = "### Security Risks\n"
            config = report.get("security_config", {})
            if config.get("install_non_market_apps") == True:
                advice += "- ⚠️ Side-loading of non-market apps is allowed (installation of unknown apks).\n"
            if config.get("mock_locations") == True:
                advice += "- ⚠️ Mock locations are enabled, exposing device location spoofing risks.\n"
            if config.get("usb_debugging") == True:
                advice += "- ⚠️ USB Debugging (ADB) is enabled, allowing shell controls over cable.\n"
                
            advice += "\n### Impact\n- USB debugging and side-loading permissions lower the device's sandboxing controls, allowing potential physical or side-loaded malware to execute code, bypass lock screens, and steal sensitive databases.\n"
            advice += "\n### Actionable Remediation Checklist\n1. Open Settings -> Developer Options -> Turn off Developer Options (or disable USB Debugging).\n2. Open Settings -> Security -> Turn off Install Unknown Apps.\n3. Audit installed third-party apps for any unrecognized software.\n"
            return advice
