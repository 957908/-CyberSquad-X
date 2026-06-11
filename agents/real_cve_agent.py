import requests


class RealCVEAgent:

    def search_cve(self, keyword):

        try:

            url = (
                "https://services.nvd.nist.gov/rest/json/cves/2.0"
                f"?keywordSearch={keyword}"
            )

            response = requests.get(
                url,
                timeout=15
            )

            data = response.json()

            results = []

            for item in data.get(
                "vulnerabilities",
                []
            )[:5]:

                cve = item["cve"]

                cve_id = cve.get(
                    "id",
                    "Unknown"
                )

                description = cve[
                    "descriptions"
                ][0]["value"]

                results.append({
                    "id": cve_id,
                    "description":
                        description[:150]
                })

            return results

        except Exception as e:

            return [{
                "error": str(e)
            }]