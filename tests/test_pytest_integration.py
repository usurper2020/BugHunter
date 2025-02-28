import pytest
from src.services.bug_bounty_analyzer import BugBountyAnalyzer
from src.services.nuclei_analyzer import NucleiAnalyzer
from src.services.ai_system import AISystem
from src.config import Config

@pytest.fixture
def setup_analyzer():
    ai_system = AISystem(Config())
    mock_nuclei = NucleiAnalyzer()
    analyzer = BugBountyAnalyzer(ai_system, mock_nuclei)
    return analyzer

def test_analyze_target(setup_analyzer):
    target_url = "https://www.hackers-island.com"
    scan_results = setup_analyzer.analyze_target(target_url)
    assert scan_results is not None
    assert 'scan_results' in scan_results

@pytest.mark.asyncio
async def test_ai_system_response(setup_analyzer):
    target_url = "https://www.hackers-island.com"
    ai_insights = await setup_analyzer.ai_system.get_response(target_url)
    assert ai_insights is not None
    assert 'ai_insights' in ai_insights
