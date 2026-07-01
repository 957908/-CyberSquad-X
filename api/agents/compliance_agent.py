class ComplianceAgent:

    def audit(
        self,
        vulnerabilities,
        security_grade,
        ssl_result
    ):

        findings = []

        # OWASP
        if len(vulnerabilities) > 0:

            findings.append({
                "framework":
                "OWASP",

                "status":
                "Non-Compliant",

                "reason":
                "Security vulnerabilities detected"
            })

        # NIST
        if security_grade["score"] < 70:

            findings.append({
                "framework":
                "NIST CSF",

                "status":
                "Partial",

                "reason":
                "Security controls insufficient"
            })

        # ISO
        if (
            ssl_result.get(
                "ssl_enabled",
                False
            ) == False
        ):

            findings.append({
                "framework":
                "ISO 27001",

                "status":
                "Non-Compliant",

                "reason":
                "SSL issue detected"
            })

        # PCI DSS
        if (
            "Admin Panel Exposed"
            in vulnerabilities
        ):

            findings.append({
                "framework":
                "PCI-DSS",

                "status":
                "Failed",

                "reason":
                "Admin access exposed"
            })

        return findings