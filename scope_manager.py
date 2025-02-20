class ScopeManager:
    """
    Manages scanning scope definitions for the BugHunter application.
    
    This class handles:
    - Defining allowed and disallowed scanning targets
    - Managing scope boundaries for security testing
    - Maintaining lists of permitted and restricted scopes
    
    The scope management ensures scans remain within authorized
    boundaries and respect defined restrictions.
    """
    
    def __init__(self):
        """
        Initialize the ScopeManager instance.
        
        Sets up empty lists for both allowed and disallowed scopes,
        providing a clean state for scope definition.
        """
        self.allowed_scopes = []
        self.disallowed_scopes = []

    def add_allowed_scope(self, scope):
        """
        Add a scope to the list of allowed targets.
        
        Parameters:
            scope (str): Target specification to allow for scanning.
                        Can be IP, domain, or URL pattern.
        """
        self.allowed_scopes.append(scope)

    def add_disallowed_scope(self, scope):
        """
        Add a scope to the list of disallowed targets.
        
        Parameters:
            scope (str): Target specification to restrict from scanning.
                        Can be IP, domain, or URL pattern.
                        
        Note:
            Disallowed scopes take precedence over allowed scopes
            when both would match a target.
        """
        self.disallowed_scopes.append(scope)

    def get_scopes(self):
        """
        Retrieve current scope definitions.
        
        Returns:
            dict: Dictionary containing two lists:
                - allowed: List of allowed scope patterns
                - disallowed: List of disallowed scope patterns
        """
        return {
            "allowed": self.allowed_scopes,
            "disallowed": self.disallowed_scopes
        }

    def clear_scopes(self):
        """
        Clear all defined scopes.
        
        Removes all entries from both allowed and disallowed
        scope lists, effectively resetting the scope configuration
        to its initial state.
        """
        self.allowed_scopes.clear()
        self.disallowed_scopes.clear()
