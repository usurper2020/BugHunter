class KnowledgeBase:
    def __init__(self):
        self.data = {}

    def add_entry(self, key, value):
        self.data[key] = value

    def get_entry(self, key):
        return self.data.get(key, None)

    def remove_entry(self, key):
        if key in self.data:
            del self.data[key]
