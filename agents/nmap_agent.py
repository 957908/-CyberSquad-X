import subprocess


class NmapAgent:

    def scan(self, target):

        if not target or target == "string":
            return "Invalid target"

        try:
            result = subprocess.check_output(
                [
                    "nmap",
                    "-Pn",
                    "-sV",
                    target
                ],
                text=True,
                stderr=subprocess.STDOUT
            )

            return result

        except Exception as e:
            return f"Nmap Error: {str(e)}"