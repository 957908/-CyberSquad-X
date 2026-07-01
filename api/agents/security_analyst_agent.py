class SecurityAnalystAgent:

    def analyze(
        self,
        risk_score,
        vulnerabilities,
        cve
    ):

        recommendations = []

        # Risk
        if risk_score >= 70:

            recommendations.append(
                "Immediate remediation required."
            )

        elif risk_score >= 40:

            recommendations.append(
                "Medium risk exposure detected."
            )

        else:

            recommendations.append(
                "Low risk exposure."
            )

        # Vulnerabilities
        for vuln in vulnerabilities:

            if (
                "Admin"
                in vuln
            ):

                recommendations.append(
                    "Restrict admin panel access."
                )

            if (
                "Login"
                in vuln
            ):

                recommendations.append(
                    "Enable MFA authentication."
                )

            if (
                "Headers"
                in vuln
            ):

                recommendations.append(
                    "Implement security headers."
                )

        # CVEs
        for item in cve:

            recommendations.append(
                f"Patch {item['cve']}"
            )

        return recommendations