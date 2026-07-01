import requests

class GeoIPAgent:

    def lookup(self, target):

        try:

            response = requests.get(
                f"http://ip-api.com/json/{target}"
            )

            return response.json()

        except Exception as e:

            return {
                "error": str(e)
            }