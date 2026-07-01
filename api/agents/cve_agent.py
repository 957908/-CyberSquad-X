class CVEAgent:

    def check(self, nmap_result):

        findings = []

        text = nmap_result.lower()

        if "apache" in text:
            findings.append({
                "service": "Apache",
                "cve": "CVE-2021-41773",
                "cvss": 9.8,
                "severity": "Critical"
            })

        if "openssh" in text:
            findings.append({
                "service": "OpenSSH",
                "cve": "CVE-2018-15473",
                "cvss": 7.5,
                "severity": "High"
            })

        if "nginx" in text:
            findings.append({
                "service": "Nginx",
                "cve": "CVE-2019-20372",
                "cvss": 6.5,
                "severity": "Medium"
            })

        return findings