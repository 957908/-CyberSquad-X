import subprocess

class NetworkScanner:

    def scan_target(self, target):

        try:
            result = subprocess.run(
                ["nmap", "-sV", target],
                capture_output=True,
                text=True
            )

            return result.stdout

        except Exception as e:
            return f"Error: {e}"