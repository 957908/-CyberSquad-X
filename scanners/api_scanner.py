import requests


class APIScanner:

    def scan(self, api_url):

        result = {}

        try:

            response = requests.get(
                api_url,
                timeout=10
            )

            result["status_code"] = (
                response.status_code
            )

            result["content_type"] = (
                response.headers.get(
                    "Content-Type",
                    "Unknown"
                )
            )

            result["server"] = (
                response.headers.get(
                    "Server",
                    "Unknown"
                )
            )

            result["https"] = (
                api_url.startswith(
                    "https"
                )
            )

            result["headers"] = dict(
                response.headers
            )

        except Exception as e:

            result["error"] = str(e)

        return result