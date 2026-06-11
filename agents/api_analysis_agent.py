class APIAnalysisAgent:

    def analyze(self, result):

        report = []

        if result.get("https"):
            report.append(
                "HTTPS: Enabled"
            )
        else:
            report.append(
                "HTTPS: Disabled"
            )

        report.append(
            f"Status Code: "
            f"{result.get('status_code')}"
        )

        report.append(
            f"Content-Type: "
            f"{result.get('content_type')}"
        )

        server = result.get(
            "server",
            "Unknown"
        )

        report.append(
            f"Server: {server}"
        )

        return "\n".join(report)