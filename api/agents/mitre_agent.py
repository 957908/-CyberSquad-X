class MitreAgent:

    def map(self,
            vulnerabilities):

        findings = []

        for vuln in vulnerabilities:

            if "Admin" in vuln:

                findings.append({
                    "technique":
                    "T1190",

                    "name":
                    "Exploit Public Facing Application"
                })

            if "Login" in vuln:

                findings.append({
                    "technique":
                    "T1078",

                    "name":
                    "Valid Accounts"
                })

        return findings