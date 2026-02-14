class NotificationService:
    def notify(self, recipient: str, event_type: str, message: str):
        """
        Simulates sending notifications via Email/SMS based on events.
        """
        print(f"--- [NOTIFICATION] ---")
        print(f"To: {recipient}")
        print(f"Event: {event_type}")
        print(f"Message: {message}")
        print(f"----------------------")
        return {
            "sent": True,
            "channel": "email",
            "timestamp": "now"
        }

notification_service = NotificationService()
