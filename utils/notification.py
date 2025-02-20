class NotificationSystem:
    """
    System for managing notifications within the BugHunter application.
    
    This class provides functionality for:
    - Managing notification subscriptions
    - Broadcasting notifications to subscribers
    - Tracking notification history
    - Monitoring system status
    
    Uses a publisher-subscriber pattern to handle notification delivery.
    """
    
    def __init__(self):
        """
        Initialize the NotificationSystem instance.
        
        Sets up:
        - Initialization state (initially False)
        - Empty list for notification history
        - Empty set for notification subscribers
        """
        self.initialized = False
        self.notifications = []
        self.subscribers = set()
        
    def initialize(self):
        """
        Initialize the notification system.
        
        Prepares the system for sending notifications by setting
        the initialization flag to True. This method must be called
        before using other notification features.
        """
        self.initialized = True
        
    def subscribe(self, subscriber):
        """
        Add a subscriber to receive notifications.
        
        Parameters:
            subscriber: Object that will receive notifications
            
        Raises:
            RuntimeError: If the notification system is not initialized
            
        Note:
            Subscribers must implement appropriate methods to
            handle received notifications.
        """
        if not self.initialized:
            raise RuntimeError("Notification system not initialized")
        self.subscribers.add(subscriber)
        
    def unsubscribe(self, subscriber):
        """
        Remove a subscriber from the notification list.
        
        Parameters:
            subscriber: Object to remove from notification list
            
        Note:
            Silently ignores attempts to unsubscribe non-existent
            subscribers for robustness.
        """
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
            
    def notify_collaborators(self, data):
        """
        Send a notification to all subscribed collaborators.
        
        Parameters:
            data: The notification data to send
            
        Returns:
            dict: Notification record containing:
                - data: The notification content
                - sent: Whether sending was successful
                - recipient_count: Number of recipients
                - timestamp: When the notification was sent
                
        Raises:
            RuntimeError: If the notification system is not initialized
        """
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
        """
        Retrieve all historical notifications.
        
        Returns:
            list: List of all notifications that have been sent,
                 in chronological order.
        """
        return self.notifications
        
    def get_status(self):
        """
        Retrieve the current status of the notification system.
        
        Returns:
            dict: Status information containing:
                - initialized: Whether system is initialized
                - notification_count: Number of sent notifications
                - subscriber_count: Number of active subscribers
                - status: Current operational status
        """
        return {
            'initialized': self.initialized,
            'notification_count': len(self.notifications),
            'subscriber_count': len(self.subscribers),
            'status': 'running' if self.initialized else 'not initialized'
        }
