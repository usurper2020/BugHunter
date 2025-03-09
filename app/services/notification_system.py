class NotificationSystem:
    def __init__(self):
        self.notifications = []

    def initialize(self):
        # Initialize the notification system
        print("Notification system initialized")

    def add_notification(self, message):
        self.notifications.append(message)
        print(f"Notification added: {message}")

    def get_notifications(self):
        return self.notifications
