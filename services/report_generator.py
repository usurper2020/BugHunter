import os
from datetime import datetime
from typing import Dict, List, Optional
import json
from fpdf import FPDF

class ReportGenerator:
    """Generates security assessment reports"""
    
    def __init__(self):
        self.reports_dir = os.path.join('data', 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_report(
        self, 
        title: str,
        findings: List[Dict],
        target_info: Dict,
        scan_info: Dict,
        output_format: str = "pdf"
    ) -> Dict:
        """Generate a security assessment report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_base = f"{title.replace(' ', '_')}_{timestamp}"
            
            if output_format.lower() == "pdf":
                return self._generate_pdf_report(
                    filename_base,
                    title,
                    findings,
                    target_info,
                    scan_info
                )
            elif output_format.lower() == "json":
                return self._generate_json_report(
                    filename_base,
                    title,
                    findings,
                    target_info,
                    scan_info
                )
            else:
                return {
                    "status": "error",
                    "message": f"Unsupported output format: {output_format}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _generate_pdf_report(
        self,
        filename_base: str,
        title: str,
        findings: List[Dict],
        target_info: Dict,
        scan_info: Dict
    ) -> Dict:
        """Generate a PDF report"""
        try:
            pdf = FPDF()
            
            # Add title page
            pdf.add_page()
            pdf.set_font("Arial", "B", 24)
            pdf.cell(0, 20, title, ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
            
            # Add target information
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Target Information", ln=True)
            pdf.set_font("Arial", "", 12)
            for key, value in target_info.items():
                pdf.cell(0, 10, f"{key}: {value}", ln=True)
                
            # Add scan information
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Scan Information", ln=True)
            pdf.set_font("Arial", "", 12)
            for key, value in scan_info.items():
                pdf.cell(0, 10, f"{key}: {value}", ln=True)
                
            # Add findings
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Findings", ln=True)
            
            for finding in findings:
                pdf.set_font("Arial", "B", 14)
                pdf.cell(0, 10, finding.get("title", "Untitled Finding"), ln=True)
                
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "Severity: " + finding.get("severity", "Unknown"), ln=True)
                
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 10, "Description: " + finding.get("description", "No description provided"))
                pdf.multi_cell(0, 10, "Impact: " + finding.get("impact", "No impact information provided"))
                pdf.multi_cell(0, 10, "Recommendation: " + finding.get("recommendation", "No recommendation provided"))
                pdf.ln(10)
                
            # Save the PDF
            filename = os.path.join(self.reports_dir, f"{filename_base}.pdf")
            pdf.output(filename)
            
            return {
                "status": "success",
                "message": "PDF report generated successfully",
                "file_path": filename
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def _generate_json_report(
        self,
        filename_base: str,
        title: str,
        findings: List[Dict],
        target_info: Dict,
        scan_info: Dict
    ) -> Dict:
        """Generate a JSON report"""
        try:
            report_data = {
                "title": title,
                "generated_at": str(datetime.now()),
                "target_info": target_info,
                "scan_info": scan_info,
                "findings": findings
            }
            
            filename = os.path.join(self.reports_dir, f"{filename_base}.json")
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2)
                
            return {
                "status": "success",
                "message": "JSON report generated successfully",
                "file_path": filename
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def get_report_list(self) -> Dict:
        """Get a list of generated reports"""
        try:
            reports = []
            for filename in os.listdir(self.reports_dir):
                file_path = os.path.join(self.reports_dir, filename)
                reports.append({
                    "filename": filename,
                    "path": file_path,
                    "size": os.path.getsize(file_path),
                    "created": datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
                })
                
            return {
                "status": "success",
                "reports": reports
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def delete_report(self, filename: str) -> Dict:
        """Delete a specific report"""
        try:
            file_path = os.path.join(self.reports_dir, filename)
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "message": "Report file not found"
                }
                
            os.remove(file_path)
            return {
                "status": "success",
                "message": "Report deleted successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
