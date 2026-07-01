import jsPDF from "jspdf";

export const generatePDF = (result) => {
  const doc = new jsPDF();

  doc.setFontSize(20);
  doc.text("CyberSquad X Security Report", 20, 20);

  doc.setFontSize(12);
  doc.text(`Risk Score: ${result.risk_score}`, 20, 40);

  doc.text("Vulnerabilities:", 20, 55);

  let y = 65;

  result.vulnerabilities?.forEach((v) => {
    doc.text(`• ${v}`, 25, y);
    y += 10;
  });

  doc.text("AI Analysis:", 20, y + 10);

  const aiText = String(result.ai_analysis || "")
    .substring(0, 1000);

  doc.text(aiText, 20, y + 20, {
    maxWidth: 170,
  });

  doc.save("CyberSquad_Report.pdf");
};