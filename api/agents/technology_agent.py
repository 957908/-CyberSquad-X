import requests

class TechnologyAgent:

    def detect(self, target):

        technologies = []

        try:

            response = requests.get(
                target,
                timeout=5
            )

            headers = response.headers
            html = response.text.lower()

            # Server Detection
            server = headers.get(
                "Server",
                ""
            )

            if server:
                technologies.append(
                    f"Server: {server}"
                )

            # Frameworks
            if "react" in html:
                technologies.append(
                    "React"
                )

            if "angular" in html:
                technologies.append(
                    "Angular"
                )

            if "vue" in html:
                technologies.append(
                    "Vue.js"
                )

            # CMS
            if "wp-content" in html:
                technologies.append(
                    "WordPress"
                )

            if "drupal" in html:
                technologies.append(
                    "Drupal"
                )

            # CDN
            if "cloudflare" in str(headers).lower():
                technologies.append(
                    "Cloudflare"
                )

            # CSS Framework
            if "bootstrap" in html:
                technologies.append(
                    "Bootstrap"
                )

            return technologies

        except Exception as e:

            return [
                f"Error: {str(e)}"
            ]