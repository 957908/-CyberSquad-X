class ReportWriterAgent:

    def generate(
        self,
        target,
        risk_score,
        vulnerabilities,
        cve,
        compliance
    ):

        report = []

        # Executive Summary
        report.append(
            f"Target {target} was analyzed."
        )

        report.append(
            f"Overall risk score is {risk_score}/100."
        )

        # Vulnerabilities
        if len(vulnerabilities) > 0:

            report.append(
                f"{len(vulnerabilities)} vulnerabilities were detected."
            )

        else:

            report.append(
                "No major vulnerabilities detected."
            )

        # CVEs
        if len(cve) > 0:

            report.append(
                f"{len(cve)} known CVEs were identified."
            )

        # Compliance
        failed = [
            x["framework"]
            for x in compliance
            if x["status"] in [
                "Failed",
                "Non-Compliant"
            ]
        ]

        if failed:

            report.append(
                "Compliance issues found in: "
                + ", ".join(failed)
            )

        # Final Recommendation
        if risk_score >= 70:

            report.append(
                "Immediate remediation is strongly recommended."
            )

        elif risk_score >= 40:

            report.append(
                "Security improvements are recommended."
            )

        else:

            report.append(
                "Current security posture appears acceptable."
            )

        return report