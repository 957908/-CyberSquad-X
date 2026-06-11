class WebsiteAnalysisAgent:

    def analyze(self, result):

        report = []

        if result.get("https"):
            report.append("HTTPS: Enabled")
        else:
            report.append("HTTPS: Disabled")

        report.append(
            f"Server: {result.get('server')}"
        )

        missing = result.get(
            "missing_headers",
            []
        )

        if missing:

            report.append(
                "\nMissing Security Headers:"
            )

            for header in missing:
                report.append(
                    f"- {header}"
                )

            report.append(
                "\nRisk Level: Medium"
            )

        else:

            report.append(
                "\nAll Security Headers Present"
            )

            report.append(
                "\nRisk Level: Low"
            )

        return "\n".join(report)