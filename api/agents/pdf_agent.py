from fpdf import FPDF


class PDFAgent:

    def generate(self, report):

        pdf = FPDF()

        pdf.add_page()

        # Title
        pdf.set_font(
            "Arial",
            "B",
            18
        )

        pdf.cell(
            0,
            10,
            "CyberSquad X Security Report",
            ln=True
        )

        pdf.ln(10)

        pdf.set_font(
            "Arial",
            "",
            12
        )

        # Executive Summary
        pdf.cell(
            0,
            10,
            f"Target: {report['target']}",
            ln=True
        )

        pdf.cell(
            0,
            10,
            f"Risk Score: {report['risk_score']}",
            ln=True
        )

        pdf.cell(
            0,
            10,
            f"Security Grade: "
            f"{report['security_grade']['grade']}",
            ln=True
        )

        pdf.ln(10)

        # Vulnerabilities
        pdf.set_font(
            "Arial",
            "B",
            14
        )

        pdf.cell(
            0,
            10,
            "Vulnerabilities",
            ln=True
        )

        pdf.set_font(
            "Arial",
            "",
            12
        )

        for vuln in report[
            "vulnerabilities"
        ]:

            pdf.cell(
                0,
                8,
                f"- {vuln}",
                ln=True
            )

        pdf.ln(5)

        # CVE
        pdf.set_font(
            "Arial",
            "B",
            14
        )

        pdf.cell(
            0,
            10,
            "CVE Findings",
            ln=True
        )

        pdf.set_font(
            "Arial",
            "",
            12
        )

        for cve in report[
            "cve"
        ]:

            pdf.cell(
                0,
                8,
                f"{cve['cve']} "
                f"({cve['severity']})",
                ln=True
            )

        pdf.ln(5)

        # OWASP
        pdf.set_font(
            "Arial",
            "B",
            14
        )

        pdf.cell(
            0,
            10,
            "OWASP",
            ln=True
        )

        pdf.set_font(
            "Arial",
            "",
            12
        )

        for item in report[
            "owasp_scan"
        ]:

            pdf.cell(
                0,
                8,
                f"{item['owasp']}",
                ln=True
            )

        pdf.output(
            "reports/executive_report.pdf"
        )

        return (
            "reports/"
            "executive_report.pdf"
        )