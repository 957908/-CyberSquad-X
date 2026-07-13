import subprocess
import json

class WindowsScanner:

    def scan(self):
        report = {}
        
        # 1. Windows Defender Status
        try:
            cmd = "Get-MpComputerStatus | Select-Object AMServiceEnabled, RealTimeProtectionEnabled, AntivirusEnabled | ConvertTo-Json"
            res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                report["defender"] = json.loads(res.stdout.strip())
            else:
                report["defender"] = {"error": res.stderr.strip() or "No output"}
        except Exception as e:
            report["defender"] = {"error": str(e)}

        # 2. Firewall Status
        try:
            cmd = "Get-NetFirewallProfile | Select-Object Name, Enabled | ConvertTo-Json"
            res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout.strip())
                if isinstance(data, dict):
                    data = [data]
                report["firewall"] = data
            else:
                report["firewall"] = {"error": res.stderr.strip() or "No output"}
        except Exception as e:
            report["firewall"] = {"error": str(e)}

        # 3. Open Listening Ports
        try:
            cmd = "Get-NetTCPConnection -State Listen | Select-Object LocalAddress, LocalPort | ConvertTo-Json"
            res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout.strip())
                if isinstance(data, dict):
                    data = [data]
                
                # Deduplicate ports list
                seen_ports = set()
                deduped = []
                for item in data:
                    port = item.get("LocalPort")
                    addr = item.get("LocalAddress")
                    if port and (port, addr) not in seen_ports:
                        seen_ports.add((port, addr))
                        deduped.append(item)
                report["open_ports"] = deduped
            else:
                report["open_ports"] = []
        except Exception as e:
            report["open_ports"] = {"error": str(e)}

        # 4. OS Version & Updates
        try:
            cmd = "[System.Environment]::OSVersion.VersionString"
            res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=5)
            report["os_version"] = res.stdout.strip() if res.returncode == 0 else "Unknown Windows Version"
            
            cmd2 = "Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 3 -Property HotFixID, Description | ConvertTo-Json"
            res2 = subprocess.run(["powershell", "-Command", cmd2], capture_output=True, text=True, timeout=5)
            if res2.returncode == 0 and res2.stdout.strip():
                patches = json.loads(res2.stdout.strip())
                if isinstance(patches, dict):
                    patches = [patches]
                report["recent_patches"] = patches
            else:
                report["recent_patches"] = []
        except Exception as e:
            report["recent_patches"] = []

        return report
