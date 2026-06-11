from datetime import datetime

class ReportAgent:

    def generate_report(
        self,
        target,
        scan_result,
        analysis
    ):

        safe_target = (
            target.replace("https://", "")
            .replace("http://", "")
            .replace("/", "_")
        )

        filename = f"report_{safe_target}.txt"

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write("=" * 60 + "\n")
            file.write("CYBERSQUAD X REPORT\n")
            file.write("=" * 60 + "\n")

            file.write(f"\nTarget: {target}\n")
            file.write(f"Date: {datetime.now()}\n")

            file.write("\nSCAN RESULTS\n")
            file.write(str(scan_result))

            file.write("\n\nANALYSIS\n")
            file.write(str(analysis))

        return filename