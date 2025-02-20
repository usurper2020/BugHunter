
import os
import yaml
import json
from typing import List, Dict, Optional
import re

class Nuclei_analyzer:
    """Class for analyzing vulnerabilities using Nuclei templates.
    
    This class provides functionality to analyze and process vulnerabilities
    based on the templates defined in the Nuclei framework.
    """
    
    def __init__(self):
        """Initialize the Nuclei analyzer with template directories."""
        self.template_dirs = [
            'nuclei-templates/cves',
            'nuclei-templates/vulnerabilities',
            'nuclei-templates/misconfiguration',
            'nuclei-templates/exposures',
            'nuclei-templates/technologies'
        ]
        self.templates = self.load_templates()
        
    def load_templates(self) -> Dict:
        """Load all Nuclei templates from the template directories."""
        templates = {}
        for dir_path in self.template_dirs:
            if os.path.exists(dir_path):
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.yaml'):
                            try:
                                with open(os.path.join(root, file), 'r') as f:
                                    template = yaml.safe_load(f)
                                    if template and 'id' in template:
                                        templates[template['id']] = {
                                            'path': os.path.join(root, file),
                                            'info': template.get('info', {}),
                                            'category': os.path.basename(root),
                                            'tags': template.get('info', {}).get('tags', []),
                                            'severity': template.get('info', {}).get('severity', 'unknown')
                                        }
                            except Exception as e:
                                print(f"Error loading template {file}: {e}")
        return templates

    def search_templates(self, query: str, category: Optional[str] = None, 
                       severity: Optional[str] = None) -> List[Dict]:
        """
        Search templates based on query, category, and severity.
        
        Args:
            query: Search terms
            category: Optional category filter
            severity: Optional severity filter
        
        Returns:
            List of matching templates with their details
        """
        results = []
        query = query.lower()
        
        for template_id, template in self.templates.items():
            # Check if template matches all criteria
            if (
                (not category or template['category'] == category) and
                (not severity or template.get('severity') == severity) and
                (query in template_id.lower() or
                 query in str(template.get('info', {})).lower() or
                 query in str(template.get('tags', [])).lower())
            ):
                results.append({
                    'id': template_id,
                    'category': template['category'],
                    'severity': template.get('severity', 'unknown'),
                    'description': template.get('info', {}).get('description', ''),
                    'tags': template.get('tags', []),
                    'path': template['path']
                })
        
        return results

    def analyze_website_content(self, url: str, content: str) -> List[Dict]:
        """
        Analyze website content against templates to suggest potential vulnerabilities.
        
        Args:
            url: Website URL
            content: Website content/source code
        
        Returns:
            List of potential vulnerability matches with template details
        """
        matches = []
        
        for template_id, template in self.templates.items():
            template_path = template['path']
            try:
                with open(template_path, 'r') as f:
                    template_data = yaml.safe_load(f)
                    
                    # Check for technology matches
                    if 'technologies' in template_data.get('info', {}).get('tags', []):
                        matchers = template_data.get('matchers', [])
                        for matcher in matchers:
                            if matcher.get('type') == 'word':
                                words = matcher.get('words', [])
                                if any(word in content for word in words):
                                    matches.append({
                                        'template_id': template_id,
                                        'category': template['category'],
                                        'severity': template.get('severity', 'unknown'),
                                        'description': template.get('info', {}).get('description', ''),
                                        'confidence': 'potential',
                                        'matched_pattern': words[0]
                                    })
                            elif matcher.get('type') == 'regex':
                                regexes = matcher.get('regex', [])
                                for regex in regexes:
                                    if re.search(regex, content):
                                        matches.append({
                                            'template_id': template_id,
                                            'category': template['category'],
                                            'severity': template.get('severity', 'unknown'),
                                            'description': template.get('info', {}).get('description', ''),
                                            'confidence': 'potential',
                                            'matched_pattern': regex
                                        })
            except Exception as e:
                print(f"Error analyzing template {template_id}: {e}")
                
        return matches

    def get_template_details(self, template_id: str) -> Optional[Dict]:
        """Get detailed information about a specific template."""
        return self.templates.get(template_id)

    def get_template_suggestions(self, url: str, technologies: List[str]) -> List[Dict]:
        """
        Get template suggestions based on detected technologies.
        
        Args:
            url: Target URL
            technologies: List of detected technologies
        
        Returns:
            List of relevant templates for testing
        """
        suggestions = []
        for tech in technologies:
            tech_lower = tech.lower()
            for template_id, template in self.templates.items():
                if (
                    tech_lower in template_id.lower() or
                    tech_lower in str(template.get('tags', [])).lower()
                ):
                    suggestions.append({
                        'id': template_id,
                        'category': template['category'],
                        'severity': template.get('severity', 'unknown'),
                        'description': template.get('info', {}).get('description', ''),
                        'tags': template.get('tags', [])
                    })
        
        return suggestions


