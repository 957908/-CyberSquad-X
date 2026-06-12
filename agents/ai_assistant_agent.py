class AIAssistantAgent:

    def generate_advice(
        self,
        target,
        risk_score,
        vulnerabilities
    ):

        report = []

        report.append(
            f"Target: {target}"
        )

        report.append(
            f"Risk Score: {risk_score}/100"
        )

        report.append(
            "\nSecurity Recommendations:"
        )

        if risk_score >= 70:

            report.append(
                "- Immediate remediation required"
            )

        elif risk_score >= 40:

            report.append(
                "- Review identified vulnerabilities"
            )

        else:

            report.append(
                "- Maintain current security posture"
            )

        for vuln in vulnerabilities:

            report.append(
                f"- Investigate: {vuln}"
            )

        return "\n".join(report)