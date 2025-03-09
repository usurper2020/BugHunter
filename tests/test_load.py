import unittest

from app.services.vulnerability_scanner import VulnerabilityScanner


class TestLoad(unittest.TestCase):
    def test_multiple_scans(self):
        scanner = VulnerabilityScanner()
        for _ in range(100):
            scanner.scan("http://example.com")
            self.assert_true(scanner.is_idle())

            if __name__ == "__main__":
                unittest.main()
