"""
Example Notification Module with Logging Implementation

This module demonstrates how to use the logging functionality
for notification services and alerts.
"""

import time
import random
from examples.from_nabil.google_api.logging_implementation import notifier_logger as logger

class NotificationService:
    """Base notification service with logging"""
    
    def __init__(self, name="Generic"):
        """Initialize notification service"""
        self.name = name
        logger.info(f"Initialized {name} notification service")
        
    def send(self, message, recipient, **kwargs):
        """
        Send notification with logging
        
        Args:
            message (str): The message to send
            recipient (str): Recipient identifier
            **kwargs: Additional notification parameters
            
        Returns:
            bool: Success status
        """
        raise NotImplementedError("Subclasses must implement send()")
        
    def _log_attempt(self, recipient, **kwargs):
        """Log notification attempt"""
        logger.info(f"Attempting to send {self.name} notification to {recipient}")
        # Log non-sensitive kwargs
        safe_kwargs = {k: v for k, v in kwargs.items() 
                       if not any(sensitive in k.lower() 
                                 for sensitive in ["token", "key", "pass", "secret"])}
        if safe_kwargs:
            logger.debug(f"Notification parameters: {safe_kwargs}")

class SlackNotifier(NotificationService):
    """Slack notification service with logging"""
    
    def __init__(self, webhook_url=None):
        """Initialize Slack notifier"""
        super().__init__("Slack")
        self.webhook_url = webhook_url
        # Mask the full URL in logs
        masked_url = "***" + webhook_url[-8:] if webhook_url else "Not configured"
        logger.debug(f"Slack webhook URL: {masked_url}")
        
    def send(self, message, channel="#general", **kwargs):
        """Send Slack notification with retry logic and logging"""
        self._log_attempt(channel, **kwargs)
        
        # Simulate sending (in a real app, use requests to post to webhook)
        max_retries = kwargs.get("max_retries", 3)
        retry_count = 0
        
        while retry_count < max_retries:
            # Simulate occasional failures for demo purposes
            success = random.random() > 0.3
            
            if success:
                logger.info(f"Slack notification sent successfully to {channel}")
                return True
            else:
                retry_count += 1
                logger.warning(f"Failed to send Slack notification, retrying... ({retry_count}/{max_retries})")
                time.sleep(1)
        
        logger.error(f"Failed to send Slack notification after {max_retries} attempts")
        return False

class EmailNotifier(NotificationService):
    """Email notification service with logging"""
    
    def __init__(self, smtp_server=None, username=None, password=None):
        """Initialize email notifier"""
        super().__init__("Email")
        self.smtp_server = smtp_server
        self.username = username
        # Don't log password, even masked
        if smtp_server:
            logger.debug(f"Configured SMTP server: {smtp_server}")
        
    def send(self, message, recipient, subject="Notification", **kwargs):
        """Send email notification with logging"""
        self._log_attempt(recipient, subject=subject, **kwargs)
        
        try:
            # In a real application, use smtplib to send actual emails
            # This is a simulation
            logger.debug(f"Preparing email with subject: {subject}")
            time.sleep(0.5)  # Simulate email sending
            
            logger.info(f"Email notification sent successfully to {recipient}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}", exc_info=True)
            return False

# Example usage
if __name__ == "__main__":
    # Slack notification example
    slack = SlackNotifier("https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX")
    slack.send("Travel time from home to work is 26 minutes", "#commute-times")
    
    # Email notification example
    email = EmailNotifier("smtp.example.com", "notifications@example.com")
    email.send(
        "Travel time from home to work is 26 minutes",
        "user@example.com",
        subject="Daily Commute Update"
    )
