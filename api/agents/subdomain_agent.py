import requests

class SubdomainAgent:

    def scan(self, domain):

        subdomains = [
            "www",
            "mail",
            "api",
            "vpn",
            "portal",
            "admin",
            "blog"
        ]

        found = []

        for sub in subdomains:

            url = f"https://{sub}.{domain}"

            try:

                response = requests.get(
                    url,
                    timeout=3
                )

                found.append({
                    "subdomain": f"{sub}.{domain}",
                    "status": response.status_code
                })

            except:
                pass

        return found