import json
import os
from datetime import datetime


class JSONReportAgent:

    def save(
        self,
        target,
        risk_score,
        website_result,
        recon_result,
        vulnerabilities,
        ai_analysis,
        crew_analysis,
        nmap_result
        
    ):

        data = {
            "target": target,
            "timestamp": str(datetime.now()),
            "risk_score": risk_score,
            "website": website_result,
             "recon": recon_result,
             "nmap": nmap_result,
             "vulnerabilities": vulnerabilities,
             "ai_analysis": ai_analysis,
             "crew_analysis": crew_analysis
}

        os.makedirs(
            "reports/history",
            exist_ok=True
        )

        # Latest Scan
        with open(
            "reports/latest_scan.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        # Historical Scan
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"reports/history/"
            f"scan_{timestamp}.json"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        return filename