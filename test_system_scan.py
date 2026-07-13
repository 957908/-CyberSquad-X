from scanners.windows_scanner import WindowsScanner
from agents.system_analyst_agent import SystemAnalystAgent
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Running Windows Scanner...")
scanner = WindowsScanner()
report = scanner.scan()

print("\n--- Telemetry Report ---")
print(json.dumps(report, indent=2))

print("\nRunning AI Security Analyst...")
analyst = SystemAnalystAgent()
advice = analyst.analyze(report, "windows")

print("\n--- AI Analyst Security Advisory ---")
print(advice)
