class NotificationSystem:
    def __init__(self):
        self.initialized = False
        self.notifications = []
        self.subscribers = set()
        
    def initialize(self):
        """Initialize notification system"""
        self.initialized = True
        
    def subscribe(self, subscriber):
        """Add a subscriber to notifications"""
        if not self.initialized:
            raise RuntimeError("Notification system not initialized")
        self.subscribers.add(subscriber)
        
    def unsubscribe(self, subscriber):
        """Remove a subscriber from notifications"""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            
    def notify_collaborators(self, data):
        """Send notification to all collaborators"""
        if not self.initialized:
            raise RuntimeError("Notification system not initialized")
            
        notification = {
            'data': data,
            'sent': True,
            'recipient_count': len(self.subscribers),
            'timestamp': None  # Could add actual timestamp if needed
        }
        
        self.notifications.append(notification)
        return notification
        
    def get_notifications(self):
        """Get all sent notifications"""
        return self.notifications
        
    def get_status(self):
        """Get the current status of notification system"""
        return {
            'initialized': self.initialized,
            'notification_count': len(self.notifications),
            'subscriber_count': len(self.subscribers),
            'status': 'running' if self.initialized else 'not initialized'
        }
