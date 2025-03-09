import unittest

from app.services.vulnerability_scanner import VulnerabilityScanner


class TestStress(unittest.TestCase):
    def test_extreme_scan(self):
        scanner = VulnerabilityScanner()
        for _ in range(1000):
            scanner.scan("http://example.com")
            self.assert_true(scanner.is_idle())

            if __name__ == "__main__":
                unittest.main()
