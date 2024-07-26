from django.db import models

from accounts.models import CustomUser

class Message(models.Model):
    author = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(CustomUser, blank=True, related_name="recipient", null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f"{self.content}"

    
