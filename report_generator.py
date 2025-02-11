import json
from datetime import datetime
import os
from fpdf import FPDF  # We'll use fpdf for PDF generation

class ReportGenerator:
    def __init__(self):
        self.reports_directory = 'reports'
        self.create_reports_directory()

    def create_reports_directory(self):
        """Create the reports directory if it doesn't exist"""
        if not os.path.exists(self.reports_directory):
            os.makedirs(self.reports_directory)

    def generate_report(self, scan_results, format='pdf'):
        """
        Generate a detailed report of the vulnerability scan findings
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_id = f"report_{timestamp}"

        if format == 'pdf':
            return self.generate_pdf_report(scan_results, report_id)
        elif format == 'json':
            return self.generate_json_report(scan_results, report_id)
        elif format == 'html':
            return self.generate_html_report(scan_results, report_id)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def generate_pdf_report(self, scan_results, report_id):
        """Generate a PDF report"""
        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Vulnerability Scan Report', 0, 1, 'C')
        pdf.ln(10)

        # Scan Information
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Scan Information', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Target: {scan_results['target']}", 0, 1)
        pdf.cell(0, 10, f"Scan ID: {scan_results['id']}", 0, 1)
        pdf.cell(0, 10, f"Timestamp: {scan_results['timestamp']}", 0, 1)
        pdf.ln(10)

        # Findings
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Findings', 0, 1)
        pdf.ln(5)

        for finding in scan_results['findings']:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, f"Type: {finding['type']}", 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 10, f"Severity: {finding['severity']}", 0, 1)
            pdf.cell(0, 10, f"Description: {finding['description']}", 0, 1)
            pdf.multi_cell(0, 10, f"Details: {finding['details']}")
            pdf.ln(5)

        # Save the PDF
        filename = os.path.join(self.reports_directory, f"{report_id}.pdf")
        pdf.output(filename)
        return filename

    def generate_json_report(self, scan_results, report_id):
        """Generate a JSON report"""
        filename = os.path.join(self.reports_directory, f"{report_id}.json")
        with open(filename, 'w') as f:
            json.dump(scan_results, f, indent=4)
        return filename

    def generate_html_report(self, scan_results, report_id):
        """Generate an HTML report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Vulnerability Scan Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .finding {{ margin: 20px 0; padding: 10px; border: 1px solid #ddd; }}
                .severity-high {{ color: red; }}
                .severity-medium {{ color: orange; }}
                .severity-low {{ color: yellow; }}
            </style>
        </head>
        <body>
            <h1>Vulnerability Scan Report</h1>
            <div class="scan-info">
                <p><strong>Target:</strong> {scan_results['target']}</p>
                <p><strong>Scan ID:</strong> {scan_results['id']}</p>
                <p><strong>Timestamp:</strong> {scan_results['timestamp']}</p>
            </div>
            <h2>Findings</h2>
        """

        for finding in scan_results['findings']:
            html_content += f"""
            <div class="finding">
                <h3>{finding['type']}</h3>
                <p class="severity-{finding['severity'].lower()}">
                    <strong>Severity:</strong> {finding['severity']}
                </p>
                <p><strong>Description:</strong> {finding['description']}</p>
                <p><strong>Details:</strong> {finding['details']}</p>
            </div>
            """

        html_content += """
        </body>
        </html>
        """

        filename = os.path.join(self.reports_directory, f"{report_id}.html")
        with open(filename, 'w') as f:
            f.write(html_content)
        return filename

    def get_report_history(self):
        """Get a list of all generated reports"""
        reports = []
        for filename in os.listdir(self.reports_directory):
            if filename.endswith(('.pdf', '.json', '.html')):
                reports.append({
                    'id': filename.split('.')[0],
                    'format': filename.split('.')[-1],
                    'path': os.path.join(self.reports_directory, filename)
                })
        return reports
