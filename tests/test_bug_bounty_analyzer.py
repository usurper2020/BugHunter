import unittest
from unittest.mock import Mock, patch
from src.services.bug_bounty_analyzer import BugBountyAnalyzer
from src.config import Config

from src.services.nuclei_analyzer import NucleiAnalyzer
from src.services.ai_system import AISystem

class TestBugBountyAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.mock_ai = Mock(spec=AISystem(Config()))

        self.mock_nuclei = Mock(spec=NucleiAnalyzer)
        self.analyzer = BugBountyAnalyzer(self.mock_ai, self.mock_nuclei)

    def test_analyze_target_basic(self):
        self.mock_nuclei.scan.return_value = {'vulnerabilities': []}
        self.mock_ai.get_response.return_value = "Test analysis"
        result = self.analyzer.analyze_target('http://test.com', 'basic')
        self.mock_nuclei.scan.assert_called_once_with(['http://test.com'])
        self.mock_ai.get_response.assert_called_once()
        self.assertIn('scan_results', result)
        self.assertIn('ai_insights', result)

    def test_analyze_target_invalid_url(self):
        result = self.analyzer.analyze_target('invalid_url', 'basic')
        self.assertIsNone(result['ai_insights'])  # Assuming it should return None for invalid URLs

    def test_analyze_target_no_ai(self):
        self.mock_nuclei.scan.return_value = {'vulnerabilities': []}
        result = self.analyzer.analyze_target('http://test.com')
        self.mock_nuclei.scan.assert_called_once_with(['http://test.com'])
        self.mock_ai.get_response.assert_not_called()
        self.assertIn('scan_results', result)
        self.assertIsNone(result['ai_insights'])

if __name__ == '__main__':
    unittest.main()
