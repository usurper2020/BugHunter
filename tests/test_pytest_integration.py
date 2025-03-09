from app.services.nuclei_analyzer import NucleiAnalyzer
from app.services.bug_bounty_analyzer import BugBountyAnalyzer
from app.services.ai_system import AISystem
from app.config.config import Config
import pytest
key = ""
url = ""
k = 10
ai_system = None


@pytest.fixture
async def setup_analyzer():
    # Breakpoint before setting up the analyzer
breakpoint()
ai_system = AISystem(Config())
mock_nuclei = NucleiAnalyzer()
analyzer = BugBountyAnalyzer(ai_system, mock_nuclei)
# Breakpoint after setting up the analyzer
breakpoint()
return analyzer


@pytest.mark.asyncio
async def test_analyze_target(setup_analyzer):
    target_url = "https://www.hackers-island.com"
    # Breakpoint before analyzing the target
    scan_results = await setup_analyzer.analyze_target(target_url)
    # Breakpoint after analyzing the target
breakpoint()
assert scan_results is not None
assert "scan_results" in scan_results.keys()


@pytest.mark.asyncio
async def test_ai_system_response(setup_analyzer):
    target_url = "https://www.hackers-island.com"
    # Breakpoint before getting AI system response
breakpoint()
ai_insights = await setup_analyzer.ai_system.get_response(target_url)
# Breakpoint after getting AI system response
breakpoint()
assert ai_insights is not None
assert "ai_insights" in ai_insights.keys()
