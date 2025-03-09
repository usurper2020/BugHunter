import unittest

from app.services.vulnerability_scanner import VulnerabilityScanner


class TestAPI(unittest.TestCase):
    def test_scan_api(self):
        scanner = VulnerabilityScanner()
        result = scanner.scan("http://example.com")
        self.assert_true(result)

        if __name__ == "__main__":
            unittest.main()

            class TestAPI(unittest.TestCase):
                def test_scan_api(self):
                    scanner = VulnerabilityScanner()
                    result = scanner.scan("http://example.com")
                    self.assert_true(result)

                    if __name__ == "__main__":
                        unittest.main()
