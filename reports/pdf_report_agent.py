from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime


class PDFReportAgent:

    def generate_pdf(
        self,
        target,
        score,
        analysis
    ):

        filename = "CyberSquad_Report.pdf"

        doc = SimpleDocTemplate(
            filename
        )

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "CyberSquad X Security Report",
                styles["Title"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

        content.append(
            Paragraph(
                f"Target: {target}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Risk Score: {score}/100",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"Generated: {datetime.now()}",
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

        content.append(
            Paragraph(
                "Analysis",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                str(analysis),
                styles["Normal"]
            )
        )

        doc.build(content)

        return filename