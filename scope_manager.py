class ScopeManager:
    def __init__(self):
        self.allowed_scopes = []
        self.disallowed_scopes = []

    def add_allowed_scope(self, scope):
        self.allowed_scopes.append(scope)

    def add_disallowed_scope(self, scope):
        self.disallowed_scopes.append(scope)

    def get_scopes(self):
        return {
            "allowed": self.allowed_scopes,
            "disallowed": self.disallowed_scopes
        }

    def clear_scopes(self):
        self.allowed_scopes.clear()
        self.disallowed_scopes.clear()
