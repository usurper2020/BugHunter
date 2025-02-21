from datetime import datetime, timedelta
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

from fpdf import FPDF
import bleach
from cryptography.fernet import Fernet
import jinja2
from sqlalchemy.orm import Session

from config import config
from logger_config import logger
from database import DatabaseManager
from models import Report, ScanResult, Finding, User
from middleware import error_handler

class ReportService:
    """Service for generating and managing vulnerability scan reports"""

    def __init__(self):
        """Initialize the ReportService with necessary directories and configurations"""
        self.reports_dir = Path('reports')
        self.templates_dir = Path('templates/reports')
        self.retention_days = config.get('REPORT_RETENTION_DAYS', 30)  # Default 30 days
        self.encrypt_reports = config.get('ENCRYPT_REPORTS', False)
        
        # Create necessary directories
        self.reports_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        
        # Initialize Jinja2 environment for HTML templates
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            autoescape=True
        )
        
        logger.info("ReportService initialized successfully")

    @error_handler
    async def generate_report(self, scan_id: str, format: str, user_id: int) -> Dict[str, Any]:
        """
        Generate a report for a vulnerability scan
        
        Args:
            scan_id: Unique identifier of the scan
            format: Report format ('pdf', 'html', or 'json')
            user_id: ID of the user requesting the report
            
        Returns:
            Dictionary containing success status, message and report details
        """
        format = format.lower()
        if format not in ('pdf', 'html', 'json'):
            return {
                'success': False,
                'message': f'Unsupported format: {format}'
            }

        async with DatabaseManager.get_session() as session:
            scan = await self._get_scan_data(session, scan_id)
            if not scan:
                return {
                    'success': False,
                    'message': 'Scan not found'
                }
            
            findings = await self._get_scan_findings(session, scan.id)
            
            try:
                report_id = self._generate_report_id()
                file_path = await self._generate_report_file(scan, findings, format, report_id)
                
                if not file_path:
                    return {
                        'success': False,
                        'message': 'Failed to generate report file'
                    }
                
                encryption_key = await self._handle_report_encryption(file_path) if self.encrypt_reports else None
                
                report = await self._create_report_record(
                    session, report_id, scan.id, format, file_path, 
                    user_id, bool(encryption_key), encryption_key
                )
                
                logger.info(f"Report generated successfully - ID: {report_id}, Format: {format}")
                
                return {
                    'success': True,
                    'message': 'Report generated successfully',
                    'report_id': report_id,
                    'file_path': str(file_path)
                }
                
            except Exception as e:
                logger.error(f"Failed to generate report: {str(e)}", exc_info=True)
                return {
                    'success': False,
                    'message': f'Failed to generate report: {str(e)}'
                }

    async def _get_scan_data(self, session: Session, scan_id: str) -> Optional[ScanResult]:
        """Retrieve scan data from database"""
        return await session.query(ScanResult).filter_by(scan_id=scan_id).first()

    async def _get_scan_findings(self, session: Session, scan_id: int) -> List[Finding]:
        """Retrieve findings for a scan from database"""
        return await session.query(Finding).filter_by(scan_id=scan_id).all()

    async def _generate_report_file(
        self, 
        scan: ScanResult, 
        findings: List[Finding],
        format: str,
        report_id: str
    ) -> Optional[Path]:
        """Generate report file in specified format"""
        generators = {
            'pdf': self._generate_pdf_report,
            'html': self._generate_html_report,
            'json': self._generate_json_report
        }
        
        generator = generators.get(format)
        if not generator:
            return None
            
        return await generator(scan, findings, report_id)

    async def _generate_pdf_report(
        self, 
        scan: ScanResult, 
        findings: List[Finding], 
        report_id: str
    ) -> Path:
        """Generate a PDF format report"""
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Vulnerability Scan Report', 0, 1, 'C')
        pdf.ln(10)
        
        # Scan Information
        self._add_scan_info_to_pdf(pdf, scan)
        
        # Findings Summary
        severity_counts = self._calculate_severity_counts(findings)
        self._add_findings_summary_to_pdf(pdf, severity_counts)
        
        # Detailed Findings
        self._add_detailed_findings_to_pdf(pdf, findings)
        
        # Save the PDF
        file_path = self.reports_dir / f"{report_id}.pdf"
        pdf.output(str(file_path))
        return file_path

    def _add_scan_info_to_pdf(self, pdf: FPDF, scan: ScanResult) -> None:
        """Add scan information section to PDF"""
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Scan Information', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Target: {scan.target_url}", 0, 1)
        pdf.cell(0, 10, f"Scan ID: {scan.scan_id}", 0, 1)
        pdf.cell(0, 10, f"Timestamp: {scan.timestamp}", 0, 1)
        pdf.ln(10)

    def _calculate_severity_counts(self, findings: List[Finding]) -> Dict[str, int]:
        """Calculate counts of findings by severity"""
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0
        }
        
        for finding in findings:
            severity_counts[finding.severity.value] += 1
            
        return severity_counts

    def _add_findings_summary_to_pdf(self, pdf: FPDF, severity_counts: Dict[str, int]) -> None:
        """Add findings summary section to PDF"""
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Findings Summary', 0, 1)
        pdf.set_font('Arial', '', 12)
        
        for severity, count in severity_counts.items():
            pdf.cell(0, 10, f"{severity.title()}: {count}", 0, 1)
        pdf.ln(10)

    def _add_detailed_findings_to_pdf(self, pdf: FPDF, findings: List[Finding]) -> None:
        """Add detailed findings section to PDF"""
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

    async def _generate_html_report(
        self, 
        scan: ScanResult, 
        findings: List[Finding], 
        report_id: str
    ) -> Path:
        """Generate an HTML format report"""
        template = self.jinja_env.get_template('report.html')
        
        severity_counts = self._calculate_severity_counts(findings)
        
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
        
        file_path = self.reports_dir / f"{report_id}.html"
        file_path.write_text(html_content, encoding='utf-8')
        
        return file_path

    async def _generate_json_report(
        self, 
        scan: ScanResult, 
        findings: List[Finding], 
        report_id: str
    ) -> Path:
        """Generate a JSON format report"""
        report_data = {
            'scan': scan.to_dict(),
            'findings': [finding.to_dict() for finding in findings],
            'generated_at': datetime.now().isoformat()
        }
        
        file_path = self.reports_dir / f"{report_id}.json"
        file_path.write_text(
            json.dumps(report_data, indent=4),
            encoding='utf-8'
        )
        
        return file_path

    async def _handle_report_encryption(self, file_path: Path) -> str:
        """Encrypt a report file and return the encryption key"""
        key = Fernet.generate_key()
        f = Fernet(key)
        
        file_data = file_path.read_bytes()
        encrypted_data = f.encrypt(file_data)
        file_path.write_bytes(encrypted_data)
        
        return key.decode()

    async def _create_report_record(
        self,
        session: Session,
        report_id: str,
        scan_id: int,
        format: str,
        file_path: Path,
        user_id: int,
        encrypted: bool,
        encryption_key: Optional[str] = None
    ) -> Report:
        """Create and save a new report record in the database"""
        report = Report(
            report_id=report_id,
            scan_id=scan_id,
            format=format,
            file_path=str(file_path),
            created_by=user_id,
            encrypted=encrypted,
            encryption_key=encryption_key
        )
        session.add(report)
        await session.commit()
        return report

    @staticmethod
    def _generate_report_id() -> str:
        """Generate a unique report ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"report_{timestamp}"

    @error_handler
    async def get_report(self, report_id: str, user_id: int) -> Dict[str, Any]:
        """
        Retrieve a generated report
        
        Args:
            report_id: Unique identifier of the report
            user_id: ID of the user requesting the report
            
        Returns:
            Dictionary containing success status, report details and file path
        """
        async with DatabaseManager.get_session() as session:
            report = await session.query(Report).filter_by(report_id=report_id).first()
            
            if not report:
                return {
                    'success': False,
                    'message': 'Report not found'
                }
            
            file_path = Path(report.file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'message': 'Report file not found'
                }
            
            return {
                'success': True,
                'report': report.to_dict(),
                'file_path': str(file_path)
            }

    @error_handler
    async def cleanup_old_reports(self) -> Dict[str, Any]:
        """
        Remove reports older than the retention period
        
        Returns:
            Dictionary containing success status and cleanup results
        """
        cleanup_date = datetime.now() - timedelta(days=self.retention_days)
        deleted_count = 0
        
        async with DatabaseManager.get_session() as session:
            old_reports = await session.query(Report).filter(
                Report.created_at < cleanup_date
            ).all()
            
            for report in old_reports:
                file_path = Path(report.file_path)
                if file_path.exists():
                    file_path.unlink()
                await session.delete(report)
                deleted_count += 1
            
            await session.commit()
        
        logger.info(f"Cleaned up {deleted_count} old reports")
        return {
            'success': True,
            'message': f'Cleaned up {deleted_count} old reports'
        }
