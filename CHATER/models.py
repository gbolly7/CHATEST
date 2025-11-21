from django.db import models
from django.conf import settings
from django.utils import timezone


User = settings.AUTH_USER_MODEL

# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    group = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, related_name='participants', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('chatroom','user')
        indexes = [
            models.Index(fields=['chatroom','user']),
        ]

    def __str__(self):
        return f"{self.user} in {self.chatroom}"
    
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['chatroom','created']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender} in {self.chatroom} at {self.created}"
    
    
