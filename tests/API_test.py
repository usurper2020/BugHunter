import unittest
from src.services.vulnerability_scanner import VulnerabilityScanner

class TestAPI(unittest.TestCase):
    def test_scan_api(self):
        scanner = VulnerabilityScanner()
        result = scanner.scan("http://example.com")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
import unittest
from src.services.vulnerability_scanner import VulnerabilityScanner

class TestAPI(unittest.TestCase):
    def test_scan_api(self):
        scanner = VulnerabilityScanner()
        result = scanner.scan("http://example.com")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
