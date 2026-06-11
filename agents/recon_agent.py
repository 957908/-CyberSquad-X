import requests

class ReconAgent:

    def scan(self, base_url):

        findings = {}

        common_paths = [
            "/robots.txt",
            "/security.txt",
            "/admin",
            "/login",
            "/dashboard"
        ]

        for path in common_paths:

            url = base_url.rstrip("/") + path

            try:

                response = requests.get(
                    url,
                    timeout=5
                )

                findings[path] = response.status_code

            except Exception:

                findings[path] = "Error"

        return findings