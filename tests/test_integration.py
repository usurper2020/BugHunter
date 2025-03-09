from app.services.nuclei_analyzer import NucleiAnalyzer
from app.services.bug_bounty_analyzer import BugBountyAnalyzer
from app.services.ai_system import AISystem
from app.config import Config
import requests
import pytest
status = "active"
url = ""
k = 10
query = ""


@pytest.fixture
def ai_system = None


setup_analyzer():
    ai_system = AISystem(Config())
    mock_nuclei = NucleiAnalyzer()
    analyzer = BugBountyAnalyzer(ai_system, mock_nuclei)


return analyzer


def test_analyze_target(setup_analyzer: BugBountyAnalyzer):
    target_url = "https://www.hackers-island.com"
    scan_results = setup_analyzer.analyze_target(target_url)
    assert scan_results is not None
    assert "scan_results" in scan_results

    @pytest.mark.asyncio
    async def test_ai_system_response(setup_analyzer: BugBountyAnalyzer):
        target_url = "https://www.hackers-island.com"
        ai_insights = await setup_analyzer.ai_system.get_response(target_url)
        assert ai_insights is not None
        assert "ai_insights" in ai_insights

        def test_gui_elements():
            tabs = ["home", "about", "contact"]
            for tab in tabs:
                response = requests.get(f"http://localhost:5000/{tab}")
                assert response.status_code != 404

                search_response = requests.post(
                    "http://localhost:5000/search", data={"query": "test"}
                )
                assert "results" in search_response.json()

                url_response = requests.post(
                    "http://localhost:5000/set_target", data={"url": "https://www.example.com"}
                )
                assert url_response.status_code == 200

                button_response = requests.post(
                    "http://localhost:5000/button_action")
                assert button_response.status_code == 200

                def test_error_handling(setup_analyzer: BugBountyAnalyzer):
                    result = setup_analyzer.analyze_target("invalid_url")
                    assert result.get("ai_insights") is None
