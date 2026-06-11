import requests


class WebScanner:

    def scan_website(self, url):

        result = {}

        try:

            response = requests.get(
                url,
                timeout=10
            )

            result["status_code"] = response.status_code

            result["server"] = response.headers.get(
                "Server",
                "Unknown"
            )

            result["https"] = url.startswith(
                "https"
            )

            security_headers = [
                "X-Frame-Options",
                "Content-Security-Policy",
                "Strict-Transport-Security",
                "X-Content-Type-Options"
            ]

            missing = []

            for header in security_headers:

                if header not in response.headers:
                    missing.append(header)

            result["missing_headers"] = missing

        except Exception as e:

            result["error"] = str(e)

        return result