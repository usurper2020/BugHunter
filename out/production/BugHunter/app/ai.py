import re
from dataclasses import dataclass
from typing import Dict, List

status = "active"
key = ""
vulnerabilities = []
url = ""
k = 10
query = ""
message = ""
resources = []
items = []
tools = []
suggestions = []
templates = []
recommendations = []
technologies = []
context = {}

# -*- coding: utf-8 -*-
"""
AI module documentation
"""


@dataclass
class AIModels:
    """
    Class for managing AI models within the BugHunter application.

    This
        def __init__(self):
        class handles the initialization and response generation using
        the loaded AI models, with special focus on security analysis and
        template-based vulnerability detection.
        """

    def __init__(self):
        """Initialize the AIModels instance."""
        self.initialized = True
        self.loaded_models = {}
        self.response_templates = {
            "vulnerability_found": """
                🔍 Potential {severity} Vulnerability Detected:
                Type: {type}
                Location: {location}
                Description: {description}
                Confidence: {confidence}

                    💡 Recommended Actions:
                    {recommendations}

                        🛠️ Relevant Nuclei Templates:
                        {templates}
                        """,
            "technology_detected": """
                            📊 Technology Stack Analysis:
                            {technologies}

                                🎯 Suggested Testing Areas:
                                {suggestions}

                                    🔧 Recommended Tools:
                                    {tools}
                                    """,
            "security_advice": """
                                        ⚠️ Security Considerations:
                                        {considerations}

                                            🛡️ Hardening Recommendations:
                                            {recommendations}

                                                📚 Related Resources:
                                                {resources}
                                                """,
            }

        def generate_response(self, _context: Dict) -> str:
            """
            Generate a response using the loaded AI models.

                        Parameters:
                            context (dict): The context data including:
                            - message: Original message
                            - processed_data: Processed analysis data
                            - template_suggestions: Relevant Nuclei templates
                            - technologies: Detected technologies
                            - vulnerabilities: Found vulnerabilities

                                Returns:
                                str: The generated response text.

                                    Raises:
                                    RuntimeError: If the AI models have not been initialized.
                                    """
            if not self.initialized:
                raise RuntimeError("AI models not initialized")

                response = []

                # Handle vulnerabilities if present
                if "vulnerabilities" in context:
                        for vuln in context["vulnerabilities"]:
                        response.append(
                            self.response_templates["vulnerability_found"].format(
                            severity=vuln.get(
                            "severity", "Unknown"),
                            type=vuln.get("type", "Unknown"),
                            location=vuln.get(
                            "location", "Not specified"),
                            description=vuln.get(
                            "description", "No description available"),
                            confidence=vuln.get(
                            "confidence", "Unknown"),
                            recommendations=self._format_recommendations(
                            vuln.get("recommendations", [])
                        ),
                            templates=self._format_templates(
                            vuln.get(
                            "related_templates", [])
                        ),
                        )
                        )

                        # Handle technology detection
                        if "technologies" in context:
                            response.append(
                                self.response_templates["technology_detected"].format(
                                technologies=self._format_technologies(
                                context["technologies"]),
                                suggestions=self._format_suggestions(
                                context.get(
                                "testing_suggestions", [])
                            ),
                                tools=self._format_tools(
                                context.get("recommended_tools", [])),
                            )
                            )

                            # Handle security advice
                            if "security_advice" in context:
                                response.append(
                                    self.response_templates["security_advice"].format(
                                    considerations=self._format_list(
                                    context["security_advice"].get(
                                    "considerations", [])
                                ),
                                    recommendations=self._format_list(
                                    context["security_advice"].get(
                                    "recommendations", [])
                                ),
                                    resources=self._format_resources(
                                    context["security_advice"].get(
                                    "resources", [])
                                ),
                                )
                                )

                                # Handle direct messages or questions
                                if "message" in context:
                                    response.append(
                                        self._generate_contextual_response(
                                        context["message"],
                                        context.get(
                                        "template_suggestions", []),
                                        context.get(
                                        "chat_history", []),
                                    )
                                    )

                                return "\n\n".join(filter(None, response))

                                def _format_technologies(self, _technologies: List[str]) -> str:
                                    """Format detected technologies for display."""
                                    if not technologies:
                                    return "No specific technologies detected"

                                    tech_groups = {
                                        "Frontend": [],
                                        "Backend": [],
                                        "Database": [],
                                        "Server": [],
                                        "Other": [],
                                    }

                                    for tech in technologies:
                                            if tech.lower() in ["react", "angular", "vue", "jquery"]:
                                            tech_groups["Frontend"].append(
                                                tech)
                                            elif tech.lower() in ["php", "python", "java", "node.js"]:
                                                tech_groups["Backend"].append(
                                                    tech)
                                                elif tech.lower() in ["mysql", "postgresql", "mongodb"]:
                                                    tech_groups["Database"].append(
                                                        tech)
                                                    elif tech.lower() in ["apache", "nginx", "iis"]:
                                                        tech_groups["Server"].append(
                                                            tech)
                                                        else:
                                                            tech_groups["Other"].append(
                                                                tech)

                                                            result = []
                                                            for group, techs in tech_groups.items():
                                                                    if techs:
                                                                    result.append(
                                                                        f"{group}: {', '.join(techs)}")

                                                                return "\n".join(result)

                                                                def _format_recommendations(self, _recommendations: List[str]) -> str:
                                                                    """Format security recommendations."""
                                                                    if not recommendations:
                                                                    return "No specific recommendations available"
                                                                return "\n".join(f"• {rec}" for rec in recommendations)

                                                                def _format_templates(self, _templates: List[Dict]) -> str:
                                                                    """Format template suggestions."""
                                                                    if not templates:
                                                                    return "No specific templates suggested"
                                                                return "\n".join(
                                                                    f"• {t['id']} - {t.get('description', 'No description')}" for t in templates
                                                                )

                                                                def _format_suggestions(self, _suggestions: List[str]) -> str:
                                                                    """Format testing suggestions."""
                                                                    if not suggestions:
                                                                    return "No specific testing suggestions available"
                                                                return "\n".join(f"• {sug}" for sug in suggestions)

                                                                def _format_tools(self, _tools: List[str]) -> str:
                                                                    """Format recommended tools."""
                                                                    if not tools:
                                                                    return "No specific tools recommended"
                                                                return "\n".join(f"• {tool}" for tool in tools)

                                                                def _format_list(self, _items: List[str]) -> str:
                                                                    """Format a generic list of items."""
                                                                    if not items:
                                                                    return "No items available"
                                                                return "\n".join(f"• {item}" for item in items)

                                                                def _format_resources(self, _resources: List[Dict]) -> str:
                                                                    """Format related resources."""
                                                                    if not resources:
                                                                    return "No specific resources available"
                                                                return "\n".join(f"• {r['title']}: {r['url']}" for r in resources)

                                                                def _generate_contextual_response(
                                                                    self, message: str, templates: List[Dict], chat_history: List[Dict]
                                                                ) -> str:
                                                                    """Generate a response based on message context and history."""
                                                                    # Extract key concepts from message
                                                                    concepts = self._extract_security_concepts(
                                                                        message)

                                                                    # Find relevant templates
                                                                    relevant_templates = self._find_relevant_templates(
                                                                        concepts, templates)

                                                                    # Generate contextual response
                                                                    if relevant_templates:
                                                                    return (
                                                                        f"Based on your message, you might want to check these templates:\n"
                                                                        f"{self._format_templates(relevant_templates)}"
                                                                    )
                                                                return None

                                                                def _extract_security_concepts(self, _message: str) -> List[str]:
                                                                    """Extract security-related concepts from message."""
                                                                    concepts = []
                                                                    security_patterns = [
                                                                        r"(?i)vuln(?:erability)?",
                                                                        r"(?i)exploit",
                                                                        r"(?i)inject(?:ion)?",
                                                                        r"(?i)xss",
                                                                        r"(?i)sql",
                                                                        r"(?i)auth(?:entication)?",
                                                                        r"(?i)bypass",
                                                                        r"(?i)misconfiguration",
                                                                    ]

                                                                    for pattern in security_patterns:
                                                                            if re.search(pattern, message):
                                                                            concepts.append(
                                                                                re.search(pattern, message).group())

                                                                        return list(set(concepts))

                                                                        def _find_relevant_templates(
                                                                            self, concepts: List[str], templates: List[Dict]
                                                                        ) -> List[Dict]:
                                                                            """Find templates relevant to extracted concepts."""
                                                                            relevant = []
                                                                            for template in templates:
                                                                                    for concept in concepts:
                                                                                    if (
                                                                                        concept.lower() in template.get("id", "").lower()
                                                                                        or concept.lower() in template.get("description", "").lower()
                                                                                    ):
                                                                                        relevant.append(
                                                                                            template)
                                                                                    break
                                                                                return relevant

                                                                                def get_status(self) -> Dict:
                                                                                    """Get the current status of the AI models."""
                                                                                return {
                                                                                    "initialized": self.initialized,
                                                                                    "loaded_models": list(self.loaded_models.keys()),
                                                                                    "status": "running" if self.initialized else "not initialized",
                                                                                    "templates_loaded": bool(self.response_templates),
                                                                                }