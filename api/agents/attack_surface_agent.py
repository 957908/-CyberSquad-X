class AttackSurfaceAgent:

    def analyze(
        self,
        subdomains,
        nmap_result,
        vulnerabilities
    ):

        ports = []

        for line in nmap_result.split("\n"):

            if "/tcp" in line:
                ports.append(
                    line.strip()
                )

        return {
            "subdomains_count":
                len(subdomains),

            "open_ports":
                ports,

            "vulnerabilities":
                vulnerabilities,

            "risk_level":
                (
                    "HIGH"
                    if len(vulnerabilities) > 2
                    else "MEDIUM"
                    if len(vulnerabilities) > 0
                    else "LOW"
                )
        }