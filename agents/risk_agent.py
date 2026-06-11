class RiskAgent:

    def calculate_risk(
        self,
        website_result,
        recon_result
    ):

        score = 0

        # Missing Headers
        score += len(
            website_result.get(
                "missing_headers",
                []
            )
        ) * 10

        # Admin/Login Exposed
        sensitive_paths = [
            "/admin",
            "/login",
            "/dashboard"
        ]

        for path in sensitive_paths:

            if recon_result.get(path) == 200:
                score += 20

        if score > 100:
            score = 100

        return score