from datetime import datetime
import asyncio
from typing import Dict, Any, List, Optional
import aiohttp
import ssl
from urllib.parse import urlparse

from config import config
from logger_config import logger_config
from database import DatabaseManager
from models import ScanResult, Finding, ScanStatus, SeverityLevel, User
from middleware import error_handler

logger = logger_config.get_logger(__name__)

class ScanService:
    """Service for handling vulnerability scanning operations"""

    def __init__(self):
        self.max_concurrent_scans = config.get('MAX_CONCURRENT_SCANS')
        self.scan_timeout = config.get('SCAN_TIMEOUT_MINUTES') * 60
        self.active_scans = 0

    @error_handler
    async def start_scan(self, target_url: str, user_id: int) -> Dict[str, Any]:
        """Start a new vulnerability scan"""
        # Validate URL
        if not self._validate_url(target_url):
            return {
                'success': False,
                'message': 'Invalid target URL'
            }

        # Check concurrent scan limit
        if self.active_scans >= self.max_concurrent_scans:
            return {
                'success': False,
                'message': 'Maximum concurrent scan limit reached'
            }

        try:
            # Create scan record
            scan_id = self._generate_scan_id()
            with DatabaseManager.get_session() as session:
                scan = ScanResult(
                    scan_id=scan_id,
                    target_url=target_url,
                    status=ScanStatus.PENDING,
                    created_by=user_id
                )
                session.add(scan)

            # Start async scan
            asyncio.create_task(self._run_scan(scan_id, target_url))

            logger.info(f"Scan started - ID: {scan_id}, Target: {target_url}")
            return {
                'success': True,
                'message': 'Scan started successfully',
                'scan_id': scan_id
            }

        except Exception as e:
            logger.error(f"Failed to start scan: {str(e)}", exc_info=True)
            return {
                'success': False,
                'message': f'Failed to start scan: {str(e)}'
            }

    async def _run_scan(self, scan_id: str, target_url: str) -> None:
        """Run the actual scan operations"""
        self.active_scans += 1
        try:
            with DatabaseManager.get_session() as session:
                scan = session.query(ScanResult).filter_by(scan_id=scan_id).first()
                scan.status = ScanStatus.RUNNING
            
            findings = []
            
            # Run security checks in parallel
            tasks = [
                self._check_security_headers(target_url),
                self._check_ssl_tls(target_url),
                self._check_common_vulnerabilities(target_url)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Scan error: {str(result)}", exc_info=True)
                else:
                    findings.extend(result)

            # Save findings
            with DatabaseManager.get_session() as session:
                scan = session.query(ScanResult).filter_by(scan_id=scan_id).first()
                
                for finding_data in findings:
                    finding = Finding(
                        scan_id=scan.id,
                        type=finding_data['type'],
                        severity=SeverityLevel(finding_data['severity']),
                        description=finding_data['description'],
                        details=finding_data.get('details')
                    )
                    session.add(finding)
                
                scan.status = ScanStatus.COMPLETED
                scan.total_findings = len(findings)
                scan.updated_at = datetime.utcnow()

            logger.info(f"Scan completed - ID: {scan_id}, Findings: {len(findings)}")

        except Exception as e:
            logger.error(f"Scan failed - ID: {scan_id}: {str(e)}", exc_info=True)
            with DatabaseManager.get_session() as session:
                scan = session.query(ScanResult).filter_by(scan_id=scan_id).first()
                scan.status = ScanStatus.FAILED
                
        finally:
            self.active_scans -= 1

    @staticmethod
    async def _check_security_headers(url: str) -> List[Dict[str, Any]]:
        """Check for security headers"""
        findings = []
        headers_to_check = {
            'X-Frame-Options': {
                'severity': 'medium',
                'description': 'Missing X-Frame-Options header'
            },
            'X-XSS-Protection': {
                'severity': 'medium',
                'description': 'Missing X-XSS-Protection header'
            },
            'X-Content-Type-Options': {
                'severity': 'medium',
                'description': 'Missing X-Content-Type-Options header'
            },
            'Content-Security-Policy': {
                'severity': 'high',
                'description': 'Missing Content-Security-Policy header'
            },
            'Strict-Transport-Security': {
                'severity': 'high',
                'description': 'Missing HSTS header'
            }
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response_headers = response.headers
                    
                    for header, config in headers_to_check.items():
                        if header not in response_headers:
                            findings.append({
                                'type': 'missing_security_header',
                                'severity': config['severity'],
                                'description': config['description'],
                                'details': f"The {header} header is missing from the response"
                            })

            except Exception as e:
                logger.error(f"Error checking security headers: {str(e)}", exc_info=True)
                findings.append({
                    'type': 'error',
                    'severity': 'high',
                    'description': 'Failed to check security headers',
                    'details': str(e)
                })

        return findings

    @staticmethod
    async def _check_ssl_tls(url: str) -> List[Dict[str, Any]]:
        """Check SSL/TLS configuration"""
        findings = []
        
        try:
            hostname = urlparse(url).netloc
            context = ssl.create_default_context()
            
            with context.wrap_socket(socket.socket(), server_hostname=hostname) as sock:
                sock.connect((hostname, 443))
                cert = sock.getpeercert()
                
                # Check certificate expiration
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                if not_after < datetime.now():
                    findings.append({
                        'type': 'ssl_certificate',
                        'severity': 'critical',
                        'description': 'SSL certificate has expired',
                        'details': f"Certificate expired on {not_after}"
                    })
                
                # Check protocol version
                version = sock.version()
                if version < ssl.TLSVersion.TLSv1_2:
                    findings.append({
                        'type': 'ssl_protocol',
                        'severity': 'high',
                        'description': 'Outdated SSL/TLS protocol version',
                        'details': f"Using {version} - TLS 1.2 or higher recommended"
                    })

        except Exception as e:
            logger.error(f"Error checking SSL/TLS: {str(e)}", exc_info=True)
            findings.append({
                'type': 'ssl_error',
                'severity': 'high',
                'description': 'Failed to check SSL/TLS configuration',
                'details': str(e)
            })

        return findings

    @staticmethod
    async def _check_common_vulnerabilities(url: str) -> List[Dict[str, Any]]:
        """Check for common vulnerabilities"""
        findings = []
        
        # Add actual vulnerability checks here
        # This is a placeholder for demonstration
        checks = [
            {
                'type': 'sql_injection',
                'severity': 'critical',
                'description': 'Potential SQL Injection vulnerability',
                'details': 'Input parameter vulnerable to SQL injection'
            },
            {
                'type': 'xss',
                'severity': 'high',
                'description': 'Cross-Site Scripting (XSS) vulnerability',
                'details': 'Reflected XSS vulnerability in search parameter'
            }
        ]
        
        findings.extend(checks)
        return findings

    @staticmethod
    def _validate_url(url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def _generate_scan_id() -> str:
        """Generate a unique scan ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"scan_{timestamp}"

    @staticmethod
    @error_handler
    def get_scan_status(scan_id: str) -> Dict[str, Any]:
        """Get the status of a scan"""
        with DatabaseManager.get_session() as session:
            scan = session.query(ScanResult).filter_by(scan_id=scan_id).first()
            
            if not scan:
                return {
                    'success': False,
                    'message': 'Scan not found'
                }
            
            return {
                'success': True,
                'status': scan.status.value,
                'total_findings': scan.total_findings,
                'timestamp': scan.timestamp.isoformat()
            }

    @staticmethod
    @error_handler
    def get_scan_results(scan_id: str) -> Dict[str, Any]:
        """Get the results of a completed scan"""
        with DatabaseManager.get_session() as session:
            scan = session.query(ScanResult).filter_by(scan_id=scan_id).first()
            
            if not scan:
                return {
                    'success': False,
                    'message': 'Scan not found'
                }
            
            if scan.status != ScanStatus.COMPLETED:
                return {
                    'success': False,
                    'message': f'Scan is {scan.status.value}'
                }
            
            findings = [finding.to_dict() for finding in scan.findings]
            
            return {
                'success': True,
                'scan': scan.to_dict(),
                'findings': findings
            }
