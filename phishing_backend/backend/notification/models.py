from django.db import models

class NotificationLog(models.Model):
    user_email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_email
