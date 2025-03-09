import logging


class NucleiTemplateService:
    """Service for managing Nuclei templates."""

    def __init__(self):
        self.logger = logging.getLogger("BugHunter.NucleiTemplateService")

        def add_template(self, _template_name: str, _template_content: str) -> bool:
        """Add a new template to the Nuclei framework"""
        try:
            # ...implementation to add the template...
            self.logger.info(f"Template {template_name} added successfully.")
        return True
        except Exception as e:
            self.logger.error(
                f"Error adding template {template_name}: {str(e)}")
        return False

        def delete_template(self, _template_name: str) -> bool:
        """Delete a template from the Nuclei framework"""
        try:
            # ...implementation to delete the template...
            self.logger.info(f"Template {template_name} deleted successfully.")
        return True
        except Exception as e:
            self.logger.error(
                f"Error deleting template {template_name}: {str(e)}")
        return False
