from datetime import datetime
import json
import os
from typing import Dict, Any, List
from fpdf import FPDF
import bleach
from cryptography.fernet import Fernet
import jinja2

from config import config
from logger_config import logger_config
from database import DatabaseManager, CacheManager
from models import Report, ScanResult, Finding, User
from middleware import error_handler

logger = logger_config.get_logger(__name__)

class ReportService:
    """Service for handling report generation and management"""

    def __init__(self):
        self.reports_dir = 'reports'
        self.templates_dir = 'templates/reports'
        self.retention_days = config.get('REPORT_RETENTION_DAYS')
        self.encrypt_reports = config.get('ENCRYPT_REPORTS')
        
        # Create necessary directories
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Initialize Jinja2 environment for HTML templates
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            autoescape=True
        )

    @error_handler
    def generate_report(self, scan_id: str, format: str, user_id: int) -> Dict[str, Any]:
        """Generate a report for a scan"""
        with DatabaseManager.get_session() as session:
            scan = session.query(ScanResult).filter_by(scan_id=scan_id).first()
            
            if not scan:
                return {
                    'success': False,
                    'message': 'Scan not found'
                }
            
            findings = session.query(Finding).filter_by(scan_id=scan.id).all()
            user = session.query(User).filter_by(id=user_id).first()
            
            # Generate report ID
            report_id = self._generate_report_id()
            
            try:
                # Generate report based on format
                if format.lower() == 'pdf':
                    file_path = self._generate_pdf_report(scan, findings, report_id)
                elif format.lower() == 'html':
                    file_path = self._generate_html_report(scan, findings, report_id)
                elif format.lower() == 'json':
                    file_path = self._generate_json_report(scan, findings, report_id)
                else:
                    return {
                        'success': False,
                        'message': f'Unsupported format: {format}'
                    }
                
                # Encrypt report if configured
                encryption_key = None
                if self.encrypt_reports:
                    encryption_key = self._encrypt_report(file_path)
                
                # Create report record
                report = Report(
                    report_id=report_id,
                    scan_id=scan.id,
                    format=format.lower(),
                    file_path=file_path,
                    created_by=user_id,
                    encrypted=bool(encryption_key),
                    encryption_key=encryption_key
                )
                session.add(report)
                
                logger.info(f"Report generated - ID: {report_id}, Format: {format}")
                
                return {
                    'success': True,
                    'message': 'Report generated successfully',
                    'report_id': report_id,
                    'file_path': file_path
                }
                
            except Exception as e:
                logger.error(f"Failed to generate report: {str(e)}", exc_info=True)
                return {
                    'success': False,
                    'message': f'Failed to generate report: {str(e)}'
                }

    def _generate_pdf_report(self, scan: ScanResult, findings: List[Finding], report_id: str) -> str:
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
        pdf.cell(0, 10, f"Target: {scan.target_url}", 0, 1)
        pdf.cell(0, 10, f"Scan ID: {scan.scan_id}", 0, 1)
        pdf.cell(0, 10, f"Timestamp: {scan.timestamp}", 0, 1)
        pdf.ln(10)
        
        # Findings Summary
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Findings Summary', 0, 1)
        pdf.set_font('Arial', '', 12)
        
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0
        }
        
        for finding in findings:
            severity_counts[finding.severity.value] += 1
        
        for severity, count in severity_counts.items():
            pdf.cell(0, 10, f"{severity.title()}: {count}", 0, 1)
        pdf.ln(10)
        
        # Detailed Findings
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Detailed Findings', 0, 1)
        pdf.ln(5)
        
        for finding in findings:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 10, f"Type: {finding.type}", 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 10, f"Severity: {finding.severity.value}", 0, 1)
            pdf.cell(0, 10, f"Description: {finding.description}", 0, 1)
            pdf.multi_cell(0, 10, f"Details: {finding.details}")
            pdf.ln(5)
        
        # Save the PDF
        file_path = os.path.join(self.reports_dir, f"{report_id}.pdf")
        pdf.output(file_path)
        return file_path

    def _generate_html_report(self, scan: ScanResult, findings: List[Finding], report_id: str) -> str:
        """Generate an HTML report"""
        template = self.jinja_env.get_template('report.html')
        
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0
        }
        
        for finding in findings:
            severity_counts[finding.severity.value] += 1
        
        html_content = template.render(
            scan=scan,
            findings=findings,
            severity_counts=severity_counts,
            generated_at=datetime.now().isoformat()
        )
        
        # Sanitize HTML content
        html_content = bleach.clean(
            html_content,
            tags=bleach.ALLOWED_TAGS + ['div', 'h1', 'h2', 'h3', 'span', 'p'],
            attributes=bleach.ALLOWED_ATTRIBUTES
        )
        
        file_path = os.path.join(self.reports_dir, f"{report_id}.html")
        with open(file_path, 'w') as f:
            f.write(html_content)
        
        return file_path

    def _generate_json_report(self, scan: ScanResult, findings: List[Finding], report_id: str) -> str:
        """Generate a JSON report"""
        report_data = {
            'scan': scan.to_dict(),
            'findings': [finding.to_dict() for finding in findings],
            'generated_at': datetime.now().isoformat()
        }
        
        file_path = os.path.join(self.reports_dir, f"{report_id}.json")
        with open(file_path, 'w') as f:
            json.dump(report_data, f, indent=4)
        
        return file_path

    def _encrypt_report(self, file_path: str) -> str:
        """Encrypt a report file"""
        key = Fernet.generate_key()
        f = Fernet(key)
        
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = f.encrypt(file_data)
        
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        
        return key.decode()

    @staticmethod
    def _generate_report_id() -> str:
        """Generate a unique report ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"report_{timestamp}"

    @error_handler
    def get_report(self, report_id: str, user_id: int) -> Dict[str, Any]:
        """Get a generated report"""
        with DatabaseManager.get_session() as session:
            report = session.query(Report).filter_by(report_id=report_id).first()
            
            if not report:
                return {
                    'success': False,
                    'message': 'Report not found'
                }
            
            if not os.path.exists(report.file_path):
                return {
                    'success': False,
                    'message': 'Report file not found'
                }
            
            return {
                'success': True,
                'report': report.to_dict(),
                'file_path': report.file_path
            }

    @error_handler
    def cleanup_old_reports(self) -> Dict[str, Any]:
        """Clean up reports older than retention period"""
        cleanup_date = datetime.now() - timedelta(days=self.retention_days)
        deleted_count = 0
        
        with DatabaseManager.get_session() as session:
            old_reports = session.query(Report).filter(
                Report.created_at < cleanup_date
            ).all()
            
            for report in old_reports:
                if os.path.exists(report.file_path):
                    os.remove(report.file_path)
                session.delete(report)
                deleted_count += 1
        
        logger.info(f"Cleaned up {deleted_count} old reports")
        return {
            'success': True,
            'message': f'Cleaned up {deleted_count} old reports'
        }
