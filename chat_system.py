class ChatSystem:
    def __init__(self):
        self.history = []

    def send_message(self, message):
        # Logic to send a message to the AI
        self.history.append(message)
        # Simulate AI response
        return "AI Response to: " + message

    def receive_message(self):
        # Logic to receive a message from the AI
        return self.history[-1] if self.history else "No messages yet."
